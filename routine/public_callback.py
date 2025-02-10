from dash import MATCH, Dash, Input, Output, callback, get_app
from dash._callback import handle_grouped_callback_args
from dash._grouping import flatten_grouping
from dash._utils import create_callback_id
from dash_auth.public_routes import PUBLIC_CALLBACKS, get_public_callbacks
from dash_pydantic_form import ModelForm


# Fix for using with DashProxy
# Can be removed when https://github.com/plotly/dash-auth/pull/163 is released
def public_callback(*callback_args, **callback_kwargs):
    """Public Dash callback.

    This works by adding the callback id (from the callback map) to a list
    of whitelisted callbacks in the Flask server's config.

    :param **: all args and kwargs passed to a dash callback
    """

    def decorator(func):
        wrapped_func = callback(*callback_args, **callback_kwargs)(func)
        output, inputs, _, _, _ = handle_grouped_callback_args(callback_args, callback_kwargs)
        if isinstance(output, Output):
            has_output = True
        else:
            output = flatten_grouping(output)
            has_output = len(output) > 0

        callback_id = create_callback_id(output, inputs, no_output=not has_output)
        try:
            app = get_app()
            app.server.config[PUBLIC_CALLBACKS] = get_public_callbacks(app) + [callback_id]
        except Exception:
            print("Could not set up the public callback as the Dash object " "has not yet been instantiated.")

        def wrap(*args, **kwargs):
            return wrapped_func(*args, **kwargs)

        return wrap

    return decorator


def add_model_form_to_public_callbacks(app: Dash):
    """Add ModelForm's server-side callback to the list of whitelisted callbacks.

    dash-pydantic-form's ModelForm uses a server-side callback to update the form's children
    which is not public by default. Since we use ModelForm to remember the email
    in the login page, we need to whitelist this callback.
    """
    callback_id = create_callback_id(
        Output(ModelForm.ids.wrapper(MATCH, MATCH, MATCH, MATCH), "children", allow_duplicate=True),
        [Input(ModelForm.ids.form(MATCH, MATCH, MATCH), "data-update")],
    )

    app.server.config[PUBLIC_CALLBACKS] = get_public_callbacks(app) + [callback_id]
