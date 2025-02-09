import dash_mantine_components as dmc


def page_loader():
    return dmc.Group(
        dmc.Loader(),
        w="100%",
        py="2rem",
        justify="center",
    )
