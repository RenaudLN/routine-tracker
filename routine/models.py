import datetime

import dash_mantine_components as dmc
from dash_iconify import DashIconify
from pydantic import BaseModel, Field

from routine.data import moods


class Food(BaseModel):
    """Food model."""

    had_breakfast: bool = Field(default=False, title="Had breakfast", repr_kwargs={"n_cols": 1.0})
    breakfast: str | None = Field(
        default=None,
        title="Breakfast",
        repr_type="Textarea",
        repr_kwargs={"visible": ("had_breakfast", "==", True), "n_cols": 1.0},
    )

    had_lunch: bool = Field(default=False, title="Had lunch", repr_kwargs={"n_cols": 1.0})
    lunch: str | None = Field(
        default=None,
        title="Lunch",
        repr_type="Textarea",
        repr_kwargs={"visible": ("had_lunch", "==", True), "n_cols": 1.0},
    )

    had_dinner: bool = Field(default=False, title="Had dinner", repr_kwargs={"n_cols": 1.0})
    dinner: str | None = Field(
        default=None,
        title="Dinner",
        repr_type="Textarea",
        repr_kwargs={"visible": ("had_dinner", "==", True), "n_cols": 1.0},
    )

    snacks: str | None = Field(
        default=None,
        title="Snacks",
        repr_type="Textarea",
        repr_kwargs={"n_cols": 1.0},
    )


class Exercise(BaseModel):
    """Exercise model."""

    name: str
    duration: int = Field(default=0, title="Duration", repr_kwargs={"placeholder": "min", "suffix": " min"}, ge=0)
    intensity: float = Field(default=0, title="Intensity", repr_type="Rating", repr_kwargs={"fractions": 2})
    Feeling: float = Field(default=0, title="Feeling", repr_type="Rating", repr_kwargs={"fractions": 2})

    def __str__(self) -> str:
        return self["name"] or "-"


class Mood(BaseModel):
    """Mood model."""

    morning: list[str] = Field(
        default_factory=list,
        repr_type="Tags",
        repr_kwargs={"n_cols": 1.0, "data": moods},
    )
    afternoon: list[str] = Field(
        default_factory=list,
        repr_type="Tags",
        repr_kwargs={"n_cols": 1.0, "data": moods},
    )
    evening: list[str] = Field(
        default_factory=list,
        repr_type="Tags",
        repr_kwargs={"n_cols": 1.0, "data": moods},
    )
    overall: float = Field(default=0, title="Rating", repr_type="Rating", repr_kwargs={"fractions": 2})
    detail: str | None = Field(default=None, repr_type="Textarea", repr_kwargs={"n_cols": 1.0})


class Sleep(BaseModel):
    """Sleep model."""

    rating: float = Field(default=0, title="Rating", repr_type="Rating", repr_kwargs={"fractions": 2})
    detail: str | None = Field(default=None, repr_type="Textarea", repr_kwargs={"n_cols": 1.0})


class Routine(BaseModel):
    """Routine model."""

    date: datetime.date = Field(default_factory=datetime.date.today)
    food: Food | None = Field(
        default=None,
        title=dmc.Group(
            [
                DashIconify(icon="fluent:food-20-regular", height=20),
                dmc.Text("Food"),
            ],
            gap="xs",
        ),
    )
    exercise: list[Exercise] = Field(
        default_factory=list,
        title=dmc.Group(
            [
                DashIconify(icon="icon-park-outline:sport", height=20),
                dmc.Text("Exercise"),
            ],
            gap="xs",
        ),
    )
    mood: Mood | None = Field(
        default=None,
        title=dmc.Group(
            [
                DashIconify(icon="tabler:mood-smile", height=20),
                dmc.Text("Mood"),
            ],
            gap="xs",
        ),
    )
    sleep: Sleep | None = Field(
        default=None,
        title=dmc.Group(
            [
                DashIconify(icon="mingcute:sleep-line", height=20),
                dmc.Text("Sleep"),
            ],
            gap="xs",
        ),
    )
