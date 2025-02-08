import dash_mantine_components as dmc
from dash import Dash, Input, Output, _dash_renderer, page_container
from dash_iconify import DashIconify

from routine import ids
from routine.components import footer_link

_dash_renderer._set_react_version("18.2.0")
app = Dash(
    __name__,
    external_stylesheets=dmc.styles.ALL,
    use_pages=True,
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
                        footer_link("Home", "carbon:home", "/"),
                        footer_link("Stats", "carbon:chart-radial", "/stats"),
                        footer_link("Profile", "carbon:user", "/profile"),
                    ],
                    h="100%",
                    px="1.5rem",
                    align="center",
                    grow=True,
                    maw="40rem",
                    mx="auto",
                ),
            ),
        ],
        header={"height": "3rem"},
        footer={"height": "3rem"},
        maw="40rem",
        mx="auto",
    ),
    theme={
        "fontFamily": "'Atkinson-HyperLegible', sans-serif",
    },
    defaultColorScheme="auto",
    id=ids.mantine_provider,
)


app.clientside_callback(
    """(isLightMode) => isLightMode ? 'light' : 'dark'""",
    Output(ids.mantine_provider, "forceColorScheme"),
    Input(ids.scheme_switch, "checked"),
    prevent_initial_callback=True,
)


if __name__ == "__main__":
    app.run(debug=True)
