import dash_mantine_components as dmc
from dash import Input, Output, callback, no_update, register_page
from dash_pydantic_form import ModelForm

from routine.db import get_db
from routine.models import Routine

register_page(__name__, path="/", title="My day", name="Home")


def layout(**_kwargs):
    """Home page layout."""
    return dmc.Box(
        p="1rem 1.5rem",
        children=[
            dmc.Title("My day", order=3, mb="1rem"),
            ModelForm(
                Routine,
                aio_id="routine",
                form_id="home",
                store_progress="local",
                restore_behavior="auto",
                fields_repr={"date": {"visible": False}},
            ),
        ],
    )


@callback(
    Output(ModelForm.ids.errors("routine", "home"), "data"),
    Input(ModelForm.ids.main("routine", "home"), "data"),
    prevent_initial_callback=True,
)
def save_my_day(data):
    if not data:
        return no_update

    try:
        routine = Routine.model_validate(data)
    except Exception as exc:
        return {":".join([str(x) for x in error["loc"]]): "Invalid value" for error in exc.errors()}

    db = get_db()
    data = routine.model_dump(mode="json")
    db.upsert(
        f"day:{data['date']}",
        data,
    )

    return None
