import dash_mantine_components as dmc
from dash import Input, Output, callback, no_update, register_page
from dash.dash import _ID_LOCATION
from dash_iconify import DashIconify
from flask import session

from routine import ids

register_page(__name__, "/profile", name="Profile")


def layout(**_kwargs):
    """Profile page layout."""

    return dmc.Stack(
        p="1rem",
        children=[
            dmc.Text(f"Logged in as {session['user']['email']}"),
            dmc.Button("Logout", id=ids.logout_btn, leftSection=DashIconify(icon="carbon:logout", height=16)),
        ],
        gap="1rem",
        align="start",
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
