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
from routine.components import CustomAccordionLayout, page_loader
from routine.db import create_day, get_dates, get_day, get_day_ref, get_latest_routine, update_day
from routine.db.routine_model import get_routine
from routine.routine_maker import RoutineMaker

# from routine.models import Routine
register_page(__name__, path="/", name="My day")


def layout(timezone: str | None = None, **_kwargs):
    """Past page layout."""
    if timezone is None:
        return page_loader()

    today = datetime.now(pytz.timezone(timezone)).strftime("%Y-%m-%d")
    db_dates = get_dates(user=session["user"]["email"])
    if today not in db_dates:
        db_dates.append(today)
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
                    offsetScrollbars=True,
                    id=ids.past_date_scroll,
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
                        dmc.Box(dmc.Skeleton(h="20rem"), id=ids.past_wrapper, mt="0.75rem"),
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
    user = session["user"]["email"]
    data = get_day(date=date, user=user)
    if data is None:
        routine_data = get_latest_routine(user)
        Routine = RoutineMaker(**routine_data).to_model()
        return ModelForm(
            Routine.model_construct(date=date, routine_ref=str(routine_data["id"])),
            aio_id="routine",
            form_id="past",
            fields_repr={"date": {"visible": False}},
            debounce_inputs=2000,
            form_layout=CustomAccordionLayout(),
        ), date

    routine_data = get_routine(data["routine_ref"])
    Routine = RoutineMaker(**routine_data).to_model()
    routine = Routine.model_validate(data)
    return ModelForm(
        routine,
        aio_id="routine",
        form_id="past",
        fields_repr={"date": {"visible": False}},
        debounce=1000,
        form_layout=CustomAccordionLayout(),
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

    routine_data = get_routine(data["routine_ref"])
    Routine = RoutineMaker(**routine_data).to_model()
    try:
        routine = Routine.model_validate(data)
    except Exception as exc:
        return {":".join([str(x) for x in error["loc"]]): "Invalid value" for error in exc.errors()}

    data = routine.model_dump(mode="json")
    data["routine_ref"] = routine_data["id"]
    user = session["user"]["email"]
    ref = get_day_ref(data["date"], user)
    if ref:
        update_day(ref, data, user)
    else:
        create_day(data, user)

    return None, data.get("date")


clientside_callback(
    ClientsideFunction(namespace="base", function_name="changePastDate"),
    Output(ids.past_date_select, "value"),
    Output(ids.past_date_btn(ALL), "className"),
    Input(ids.past_date_btn(ALL), "n_clicks"),
    State(ids.past_date_btn(ALL), "id"),
    prevent_initial_call=True,
)


clientside_callback(
    ClientsideFunction(namespace="base", function_name="scrollToLatest"),
    Output(ids.past_date_scroll, "className"),
    Input(ids.past_date_scroll, "id"),
)
