from datetime import date

import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, register_page
from dash_pydantic_form import ModelForm
from surrealdb import RecordID

from routine import ids
from routine.db import get_db
from routine.models import Routine

register_page(__name__, path="/past", title="Past", name="Past")


def layout(**_kwargs):
    """Past page layout."""

    return (
        dmc.Box(
            p="1rem 1.5rem",
            children=[
                dmc.DateInput(
                    value=date.today().strftime("%Y-%m-%d"),
                    id=ids.past_date_select,
                    valueFormat="YYYY-MM-DD",
                ),
                dcc.Loading(
                    dmc.Box(dmc.Skeleton(h="20rem"), id=ids.past_wrapper, mt="2rem"),
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
    data = db.select(RecordID("day", date))
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
