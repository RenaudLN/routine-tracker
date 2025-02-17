from datetime import datetime

import dash_mantine_components as dmc
import pytz
from dash import Input, Output, State, callback, no_update, register_page
from dash.dash import _ID_LOCATION
from dash_iconify import DashIconify
from dash_pydantic_form import ModelForm
from flask import session

from routine import ids
from routine.db import count_days_using_routine, create_routine, get_latest_routine, update_routine
from routine.db.day import get_day_ref, merge_day
from routine.routine_maker import RoutineMaker, field_options

register_page(__name__, "/profile", name="Profile")


def layout(timezone: str | None = None, **_kwargs):
    """Profile page layout."""

    routine_data = get_latest_routine(session["user"]["email"])
    if routine_data is None:
        # TODO: Default routine
        pass

    routine_maker = RoutineMaker(**routine_data)

    return dmc.Stack(
        p="1rem",
        children=[
            dmc.Text(f"Logged in as {session['user']['email']}"),
            dmc.Text(f"Time zone: {timezone}", size="xs", c="dimmed", mt="-1rem"),
            dmc.Box(
                dmc.Button("Logout", id=ids.logout_btn, leftSection=DashIconify(icon="carbon:logout", height=16)),
            ),
            dmc.Space(h="sm"),
            dmc.Title("My Routine", order=3),
            ModelForm(
                routine_maker,
                aio_id="routine",
                form_id="maker",
                debounce=1000,
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
            dmc.Box(
                dmc.Button("Save", id=ids.save_routine_btn, leftSection=DashIconify(icon="carbon:save", height=16)),
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


@callback(
    Output(ModelForm.ids.errors("routine", "maker"), "data"),
    Input(ids.save_routine_btn, "n_clicks"),
    State(ModelForm.ids.main("routine", "maker"), "data"),
    State(ids.client_timezone, "data"),
    prevent_initial_call=True,
    running=[Output(ids.save_routine_btn, "loading"), True, False],
)
def save_routine(n_clicks, data, timezone):
    if not n_clicks:
        return no_update
    try:
        routine_maker = RoutineMaker.model_validate(data)
    except Exception as exc:
        return {":".join([str(x) for x in error["loc"]]): "Invalid value" for error in exc.errors()}

    user = session["user"]["email"]
    today = datetime.now(pytz.timezone(timezone)).strftime("%Y-%m-%d")
    routine_ref = get_latest_routine(user)["id"]
    count = count_days_using_routine(routine_ref, today)
    if count > 0:
        routine_ref = create_routine(routine_maker.model_dump(mode="json"), user)
        today_ref = get_day_ref(today, user)
        if today_ref is not None:
            merge_day(today_ref, {"routine_ref": routine_ref})
    else:
        update_routine(routine_ref, routine_maker.model_dump(mode="json"), user)

    return None
