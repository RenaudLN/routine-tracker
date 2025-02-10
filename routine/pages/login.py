import logging
import os

import dash_mantine_components as dmc
import requests
from dash import Input, Output, State, no_update, register_page
from dash.dash import _ID_LOCATION
from dash_pydantic_form import ModelForm
from flask import session
from pydantic import BaseModel, Field, field_validator

from routine import ids
from routine.public_callback import public_callback

register_page(__name__, "/login", title="Login | Routine")


class LoginData(BaseModel):
    """Login data model."""

    email: str = Field(default=None, pattern="^[^@]+@[^@]+\.[^@]+$")
    password: str = Field(default=None, repr_type="Password")

    @field_validator("email")
    def validate_email(cls, value):
        """Validate email."""
        if not value:
            raise ValueError("Email is required")
        return value


login_form = ModelForm(
    LoginData,
    aio_id="login",
    form_id="login-form",
    container_kwargs={"style": {"width": "100%"}},
    submit_on_enter=True,
    store_progress=False,
    restore_behavior="auto",
)


def layout(**_kwargs):
    """Base login layout, shared between login and login password.

    NOTE: other_children are positioned between the form and the login button
    """
    return dmc.Modal(
        size="sm",
        closeOnClickOutside=False,
        closeOnEscape=False,
        withCloseButton=False,
        opened=True,
        centered=True,
        radius="md",
        overlayProps={
            "bg": "color-mix(in srgb, var(--mantine-color-body), var(--mantine-color-text) 5%)",
        },
        children=[
            dmc.Stack(
                [
                    dmc.Group(
                        [
                            dmc.Image(src="/assets/logo.svg", w="2.5rem"),
                            dmc.Title("Welcome to Routine", order=3, my="1rem 0.5rem"),
                        ],
                    ),
                    login_form,
                    # dmc.Checkbox(
                    #     "Remember me",
                    #     id=ids.login_remember,
                    #     persistence=True,
                    #     style={"alignSelf": "start"},
                    # ),
                    dmc.Button("Log in", id=ids.login_btn, style={"alignSelf": "stretch"}),
                ],
                align="center",
            ),
        ],
    )


@public_callback(
    Output(_ID_LOCATION, "href", allow_duplicate=True),
    Output(login_form.ids.errors, "data", allow_duplicate=True),
    Input(ids.login_btn, "n_clicks"),
    Input(login_form.ids.form, "data-submit"),
    State(login_form.ids.main, "data"),
    prevent_initial_call=True,
    running=[(Output(ids.login_btn, "loading"), True, False)],
)
def sign_in_with_password(_t1, _t2, form_data: dict):
    """Sign in with password."""
    if not form_data or not form_data.get("password"):
        return no_update

    api_key = os.getenv("FIREBASE_API_KEY")
    try:
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}",
            data={"email": form_data["email"], "password": form_data["password"], "returnSecureToken": True},
            timeout=10,
        )
    except requests.exceptions.Timeout:
        logging.exception("Failed to sign in after timeout")
        return no_update, {"password": "Request timed out"}
    except Exception:
        logging.exception("Failed to sign in with unknown error")
        return no_update, {"password": "An error occurred, please try again"}

    if not response.ok:
        return no_update, {"password": "Invalid email or password"}

    try:
        content = response.json()
    except Exception:
        logging.exception("Failed to sign in with unknown error")
        return no_update, {"password": "An error occurred, please try again"}

    session["user"] = {"email": content["email"]}
    return "/", no_update


# # Toggle the 'remember email' behaviour
# clientside_callback(
#     ClientsideFunction(namespace="base", function_name="switchRememberMe"),
#     Output(login_form.ids.form, "data-storeprogress"),
#     Output(login_form.ids.form, "data-getvalues"),
#     Input(ids.login_remember, "checked"),
# )
