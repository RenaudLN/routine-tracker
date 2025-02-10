from datetime import datetime

import dash_mantine_components as dmc
import pytz
from dash import ALL, ClientsideFunction, Input, Output, State, callback, clientside_callback, dcc, html, register_page
from dash_pydantic_form import ModelForm
from flask import session

from routine import ids
from routine.components import page_loader
from routine.db import get_db
from routine.models import Routine

register_page(__name__, path="/past", name="Past")


def layout(timezone: str | None = None, **_kwargs):
    """Past page layout."""
    if timezone is None:
        return page_loader()

    today = datetime.now(pytz.timezone(timezone)).strftime("%Y-%m-%d")
    db = get_db()
    available_dates = [
        datetime.strptime(val, "%Y-%m-%d")
        for val in db.query(
            "SELECT VALUE date FROM day WHERE user = $user ORDER BY date",
            {"user": session["user"]["email"]},
        )
    ]

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
                dcc.Loading(
                    dmc.Box(dmc.Skeleton(h="20rem"), id=ids.past_wrapper, mt="1.5rem"),
                    custom_spinner=page_loader(),
                ),
            ],
        ),
    )


@callback(
    Output(ids.past_wrapper, "children"),
    Input(ids.past_date_select, "value"),
)
def update_past(date):
    db = get_db()
    data = db.query(
        "SELECT * FROM ONLY day WHERE date = $date AND user = $user LIMIT 1",
        {"date": date, "user": session["user"]["email"]},
    )
    if data is None:
        return dmc.Alert(f"No data for {date}", color="teal")
    routine = Routine.model_validate(data)
    return ModelForm(
        routine,
        aio_id="routine",
        form_id="past",
        read_only=True,
        excluded_fields=["date"],
    )


clientside_callback(
    ClientsideFunction(namespace="base", function_name="changePastDate"),
    Output(ids.past_date_select, "value"),
    Output(ids.past_date_btn(ALL), "className"),
    Input(ids.past_date_btn(ALL), "n_clicks"),
    State(ids.past_date_btn(ALL), "id"),
    prevent_initial_call=True,
)
