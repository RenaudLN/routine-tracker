import dash_mantine_components as dmc
from dash import Input, Output, callback, no_update, register_page
from dash.dash import _ID_LOCATION
from dash_iconify import DashIconify
from dash_pydantic_form import ModelForm
from flask import session

from routine import ids
from routine.routine_maker import RoutineMaker, field_options

register_page(__name__, "/profile", name="Profile")


def layout(**_kwargs):
    """Profile page layout."""

    return dmc.Stack(
        p="1rem",
        children=[
            dmc.Text(f"Logged in as {session['user']['email']}"),
            dmc.Box(
                dmc.Button("Logout", id=ids.logout_btn, leftSection=DashIconify(icon="carbon:logout", height=16)),
            ),
            dmc.Space(h="sm"),
            ModelForm(
                RoutineMaker,
                aio_id="routine",
                form_id="maker",
                fields_repr={
                    "blocks": {
                        "fields_repr": {
                            "fields": {
                                "fields_repr": {
                                    "type_": {
                                        "title": "",
                                        "data": field_options,
                                        "searchable": True,
                                    },
                                    "fields": {
                                        "fields_repr": {
                                            "type_": {
                                                "title": "",
                                                "data": [o for o in field_options if o["value"] != "list"],
                                                "searchable": True,
                                            }
                                        }
                                    },
                                },
                            },
                        },
                    },
                },
            ),
        ],
        gap="1rem",
        align="stretch",
    )


@callback(
    Output(_ID_LOCATION, "href", allow_duplicate=True),
    Input(ids.logout_btn, "n_clicks"),
    prevent_initial_call=True,
)
def logout(n_clicks):
    if not n_clicks:
        return no_update
    session.clear()
    return "/login"
