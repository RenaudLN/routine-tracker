import dash_mantine_components as dmc
from dash import register_page
from dash_pydantic_form import ModelForm

from routine.models import Routine

register_page(__name__, path="/", title="My day", name="Home")


def layout(**_kwargs):
    return (
        dmc.Box(
            p="1rem 1.5rem",
            children=[
                dmc.Title("My day", order=3, mb="1rem"),
                ModelForm(
                    Routine,
                    aio_id="routine",
                    form_id="home",
                    store_progress="local",
                    restore_behavior="auto",
                    debounce_inputs=500,
                ),
            ],
        ),
    )
