# from datetime import date, datetime

# import dash_mantine_components as dmc
# import pytz
# from dash import Input, Output, callback, no_update, register_page
# from dash_pydantic_form import ModelForm
# from dash_pydantic_utils import model_construct_recursive
# from flask import session

# from routine.components import page_loader
# from routine.db import get_db
# from routine.models import Routine

# register_page(__name__, path="/", name="My day")


# def layout(timezone: str | None = None, **_kwargs):
#     """Home page layout."""
#     if timezone is None:
#         return page_loader()

#     today = datetime.now(pytz.timezone(timezone)).strftime("%Y-%m-%d")

#     db = get_db()
#     data = db.query(
#         "SELECT * FROM ONLY day WHERE date = $date AND user = $user LIMIT 1",
#         {"date": today, "user": session["user"]["email"]},
#     )

#     routine = (
#         model_construct_recursive(data, Routine) if data is not None else Routine.model_construct(date=date.today())
#     )
#     return dmc.Box(
#         p="1rem",
#         children=[
#             dmc.Title("My day", order=3, mb="1rem"),
#             ModelForm(
#                 routine,
#                 aio_id="routine",
#                 form_id="home",
#                 fields_repr={"date": {"visible": False}},
#                 debounce=1500,
#             ),
#         ],
#     )


# @callback(
#     Output(ModelForm.ids.errors("routine", "home"), "data"),
#     Input(ModelForm.ids.main("routine", "home"), "data"),
#     prevent_initial_callback=True,
# )
# def save_my_day(data):
#     if not data:
#         return no_update

#     try:
#         routine = Routine.model_validate(data)
#     except Exception as exc:
#         return {":".join([str(x) for x in error["loc"]]): "Invalid value" for error in exc.errors()}

#     db = get_db()
#     data = routine.model_dump(mode="json")
#     res = db.query(
#         "SELECT id FROM ONLY day WHERE date = $date AND user = $user LIMIT 1",
#         {"date": data["date"], "user": session["user"]["email"]},
#     )
#     if res:
#         db.update(res["id"], data | {"user": session["user"]["email"]})
#     else:
#         db.create("day", data | {"user": session["user"]["email"]})

#     return None
