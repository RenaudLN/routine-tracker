import dash_mantine_components as dmc
from dash_iconify import DashIconify


def footer_link(label: str, icon: str, href: str):
    """Footer link."""
    return dmc.Anchor(
        dmc.Stack(
            [DashIconify(icon=icon, height=16), dmc.Text(label, size="xs", c="dimmed")],
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
    )
