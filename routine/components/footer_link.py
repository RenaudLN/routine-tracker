import dash_mantine_components as dmc
from dash import ALL, ClientsideFunction, Input, Output, State, clientside_callback
from dash.dash import _ID_LOCATION
from dash_iconify import DashIconify

from routine import ids


def footer_link(label: str, icon: str, href: str):
    """Footer link."""
    return dmc.Anchor(
        dmc.Stack(
            [DashIconify(icon=icon, height=16, id=ids.footer_link_icon(href)), dmc.Text(label, size="xs", c="dimmed")],
            pt="0.125rem",
            gap="0.125rem",
            align="center",
            h="100%",
            justify="center",
        ),
        href=href,
        c="inherit",
        underline=False,
        h="100%",
        className="footer-link",
        id=ids.footer_link(href),
    )


clientside_callback(
    ClientsideFunction(namespace="base", function_name="highlightLink"),
    Output(ids.footer_link(ALL), "className"),
    Output(ids.footer_link_icon(ALL), "icon"),
    Input(_ID_LOCATION, "pathname"),
    State(ids.footer_link(ALL), "id"),
    State(ids.footer_link_icon(ALL), "icon"),
)
