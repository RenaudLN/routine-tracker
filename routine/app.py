import os
from contextlib import suppress

import dash_mantine_components as dmc
from dash import ClientsideFunction, Dash, Input, Output, _dash_renderer, dcc, page_container
from dash_auth import OIDCAuth
from dash_iconify import DashIconify

from routine import ids
from routine.components import footer_link

with suppress(ModuleNotFoundError):
    import dotenv

    dotenv.load_dotenv()


_dash_renderer._set_react_version("18.2.0")
app = Dash(
    __name__,
    external_stylesheets=dmc.styles.ALL,
    use_pages=True,
    routing_callback_inputs={
        "timezone": Input(ids.client_timezone, "data"),
    },
    suppress_callback_exceptions=True,
)
server = app.server

OIDCAuth(
    app=app,
    secret_key=os.getenv("SECRET_KEY"),
    idp_selection_route="/login",
    public_routes=["/login"],
    logout_route="/logout",
)

app.layout = dmc.MantineProvider(
    dmc.AppShell(
        [
            dmc.AppShellHeader(
                dmc.Group(
                    [
                        dmc.Text("Routine", size="lg", fw="bold"),
                        dmc.Switch(
                            offLabel=DashIconify(icon="radix-icons:moon", height=18),
                            onLabel=DashIconify(icon="radix-icons:sun", height=18),
                            size="md",
                            color="yellow",
                            persistence=True,
                            checked=True,
                            id=ids.scheme_switch,
                        ),
                    ],
                    h="100%",
                    px="1.5rem",
                    align="center",
                    justify="space-between",
                    maw="40rem",
                    mx="auto",
                ),
            ),
            dmc.AppShellMain(page_container),
            dmc.AppShellFooter(
                dmc.Group(
                    [
                        footer_link("My day", "fluent:home-16-regular", "/"),
                        footer_link("Past", "fluent:calendar-16-regular", "/past"),
                        footer_link("Stats", "fluent:chart-multiple-16-regular", "/stats"),
                        footer_link("Profile", "fluent:person-16-regular", "/profile"),
                    ],
                    h="100%",
                    px="1.5rem",
                    align="center",
                    grow=True,
                    maw="40rem",
                    mx="auto",
                ),
            ),
            dmc.NotificationProvider(position="top-right"),
            dmc.Box(id=ids.notifications_wrapper),
            dcc.Store(id=ids.client_timezone),
        ],
        header={"height": "3rem"},
        footer={"height": "3rem"},
        maw="40rem",
        mx="auto",
    ),
    theme={
        "fontFamily": "'Atkinson-HyperLegible', sans-serif",
        "primaryColor": "yellow",
        "defaultRadius": "md",
        "components": {
            "Accordion": {
                "defaultProps": {
                    "style": {"display": "flex", "flexDirection": "column", "gap": "0.5rem"},
                },
            },
            "AccordionPanel": {
                "defaultProps": {"pt": "0.5rem"},
            },
            "AccordionItem": {
                "defaultProps": {
                    "bg": "color-mix(in srgb, var(--mantine-color-gray-light), #0000 90%)",
                    "bd": "1px solid var(--mantine-color-gray-light)",
                    "style": {"borderRadius": "calc(0.75rem * var(--mantine-scale))"},
                    "mb": 0,
                },
            },
            "AccordionControl": {
                "defaultProps": {
                    "style": {"borderRadius": "calc(0.75rem * var(--mantine-scale))"},
                },
            },
            "TextInput": {
                "defaultProps": {"debounce": True},
            },
            "NumberInput": {
                "defaultProps": {"debounce": True},
            },
            "Textarea": {
                "defaultProps": {"debounce": True},
            },
        },
    },
    defaultColorScheme="auto",
    id=ids.mantine_provider,
)


app.clientside_callback(
    ClientsideFunction(namespace="base", function_name="switchScheme"),
    Output(ids.mantine_provider, "forceColorScheme"),
    Input(ids.scheme_switch, "checked"),
    prevent_initial_callback=True,
)

app.clientside_callback(
    ClientsideFunction(namespace="base", function_name="getTimezone"),
    Output(ids.client_timezone, "data"),
    Input(ids.client_timezone, "id"),
)


if __name__ == "__main__":
    app.run(debug=True)
