import dash_mantine_components as dmc
from dash import Dash, Input, Output, _dash_renderer, page_container
from dash_iconify import DashIconify

from routine import ids

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
                ),
            ),
            dmc.AppShellMain(page_container),
            dmc.AppShellFooter(
                dmc.Group(
                    [
                        dmc.Anchor(
                            dmc.Stack(
                                [DashIconify(icon="carbon:home", height=16), dmc.Text("Home", size="xs", c="dimmed")],
                                gap="0.125rem",
                                align="center",
                            ),
                            href="/",
                            c="inherit",
                            underline=False,
                        ),
                        dmc.Anchor(
                            dmc.Stack(
                                [
                                    DashIconify(icon="carbon:chart-radial", height=16),
                                    dmc.Text("Stats", size="xs", c="dimmed"),
                                ],
                                gap="0.125rem",
                                align="center",
                            ),
                            href="/stats",
                            c="inherit",
                            underline=False,
                        ),
                        dmc.Anchor(
                            dmc.Stack(
                                [
                                    DashIconify(icon="carbon:user", height=16),
                                    dmc.Text("Profile", size="xs", c="dimmed"),
                                ],
                                gap="0.125rem",
                                align="center",
                            ),
                            href="/profile",
                            c="inherit",
                            underline=False,
                        ),
                    ],
                    h="100%",
                    px="1.5rem",
                    align="center",
                    justify="space-around",
                ),
            ),
        ],
        header={"height": "3rem"},
        footer={"height": "3rem"},
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
