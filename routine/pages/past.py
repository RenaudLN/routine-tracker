from datetime import datetime

import dash_mantine_components as dmc
import pytz
from dash import (
    ALL,
    ClientsideFunction,
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    dcc,
    html,
    no_update,
    register_page,
)
from dash_pydantic_form import ModelForm
from flask import session

from routine import ids
from routine.components import page_loader
from routine.db import get_db
from routine.models import Routine

register_page(__name__, path="/", name="My day")


def layout(timezone: str | None = None, **_kwargs):
    """Past page layout."""
    if timezone is None:
        return page_loader()

    today = datetime.now(pytz.timezone(timezone)).strftime("%Y-%m-%d")
    db = get_db()
    db_dates = db.query(
        "SELECT VALUE date FROM day WHERE user = $user ORDER BY date LIMIT 31",
        {"user": session["user"]["email"]},
    )
    available_dates = [datetime.strptime(val, "%Y-%m-%d") for val in db_dates]

    return (
        dmc.Box(
            p="1rem",
            children=[
                dmc.ScrollArea(
                    dmc.Group(
                        [
                            html.Div(
                                dmc.Stack(
                                    [
                                        dmc.Text(date.strftime("%d"), fw="bold"),
                                        dmc.Text(date.strftime("%b"), size="sm"),
                                    ],
                                    gap=0,
                                    align="center",
                                ),
                                className="date-btn" + (" active" if date.strftime("%Y-%m-%d") == today else ""),
                                id=ids.past_date_btn(date.strftime("%Y-%m-%d")),
                            )
                            for date in available_dates
                        ],
                        justify="center",
                        wrap="nowrap",
                    ),
                ),
                dmc.DateInput(
                    value=today,
                    id=ids.past_date_select,
                    valueFormat="YYYY-MM-DD",
                    display="none",
                ),
                dmc.Box(
                    [
                        dmc.LoadingOverlay(id=ids.past_overlay, visible=False),
                        dmc.Box(dmc.Skeleton(h="20rem"), id=ids.past_wrapper, mt="1.5rem"),
                        dcc.Store(id=ids.past_previous_date, data=None),
                    ],
                    pos="relative",
                ),
            ],
        ),
    )


@callback(
    Output(ids.past_wrapper, "children"),
    Output(ids.past_previous_date, "data"),
    Input(ids.past_date_select, "value"),
    running=[(Output(ids.past_overlay, "visible"), True, False)],
)
def update_past(date):
    db = get_db()
    data = db.query(
        "SELECT * FROM ONLY day WHERE date = $date AND user = $user LIMIT 1",
        {"date": date, "user": session["user"]["email"]},
    )
    if data is None:
        return dmc.Alert(f"No data for {date}", color="teal"), None
    routine = Routine.model_validate(data)
    return ModelForm(
        routine,
        aio_id="routine",
        form_id="past",
        fields_repr={"date": {"visible": False}},
        debounce_inputs=2000,
    ), None


@callback(
    Output(ModelForm.ids.errors("routine", "past"), "data"),
    Output(ids.past_previous_date, "data", allow_duplicate=True),
    Input(ModelForm.ids.main("routine", "past"), "data"),
    State(ids.past_previous_date, "data"),
    prevent_initial_call=True,
)
def save_my_day(data, previous_date):
    if not data:
        return no_update

    if data.get("date") != previous_date:
        return no_update, data.get("date")

    try:
        routine = Routine.model_validate(data)
    except Exception as exc:
        return {":".join([str(x) for x in error["loc"]]): "Invalid value" for error in exc.errors()}

    db = get_db()
    data = routine.model_dump(mode="json")
    res = db.query(
        "SELECT id FROM ONLY day WHERE date = $date AND user = $user LIMIT 1",
        {"date": data["date"], "user": session["user"]["email"]},
    )
    if res:
        db.update(res["id"], data | {"user": session["user"]["email"]})
    else:
        db.create("day", data | {"user": session["user"]["email"]})

    return None, data.get("date")


clientside_callback(
    ClientsideFunction(namespace="base", function_name="changePastDate"),
    Output(ids.past_date_select, "value"),
    Output(ids.past_date_btn(ALL), "className"),
    Input(ids.past_date_btn(ALL), "n_clicks"),
    State(ids.past_date_btn(ALL), "id"),
    prevent_initial_call=True,
)
