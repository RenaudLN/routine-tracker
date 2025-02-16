import datetime

import dash_mantine_components as dmc
from dash_iconify import DashIconify
from pydantic import BaseModel, Field

from routine.data import moods


class Food(BaseModel):
    """Food model."""

    had_breakfast: bool = Field(default=False, title="Breakfast", repr_kwargs={"n_cols": 1.0})
    breakfast: str | None = Field(
        default=None,
        title="",
        repr_type="Textarea",
        repr_kwargs={"visible": ("had_breakfast", "==", True), "n_cols": 1.0},
    )

    had_lunch: bool = Field(default=False, title="Lunch", repr_kwargs={"n_cols": 1.0})
    lunch: str | None = Field(
        default=None,
        title="",
        repr_type="Textarea",
        repr_kwargs={"visible": ("had_lunch", "==", True), "n_cols": 1.0},
    )

    had_dinner: bool = Field(default=False, title="Dinner", repr_kwargs={"n_cols": 1.0})
    dinner: str | None = Field(
        default=None,
        title="",
        repr_type="Textarea",
        repr_kwargs={"visible": ("had_dinner", "==", True), "n_cols": 1.0},
    )

    snacks: str | None = Field(
        default=None,
        title="Snacks",
        repr_type="Textarea",
        repr_kwargs={"n_cols": 1.0},
    )


class Activity(BaseModel):
    """Activity model"""

    name: str
    duration: int = Field(default=0, title="Duration", repr_kwargs={"placeholder": "min", "suffix": " min"}, ge=0)
    intensity: float = Field(
        default=0, title="Intensity", repr_type="Rating", repr_kwargs={"fractions": 2, "size": "xl"}
    )
    Feeling: float = Field(default=0, title="Feeling", repr_type="Rating", repr_kwargs={"fractions": 2, "size": "xl"})

    def __str__(self) -> str:
        return self["name"] or "-"


class Exercise(BaseModel):
    """Exercise model."""

    activities: list[Activity] = Field(
        default_factory=list,
    )
    steps: int = Field(default=0, ge=0)


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
    overall: float = Field(default=0, repr_type="Rating", repr_kwargs={"fractions": 2, "size": "xl"})
    detail: str | None = Field(default=None, repr_type="Textarea", repr_kwargs={"n_cols": 1.0})


class Sleep(BaseModel):
    """Sleep model."""

    rating: float = Field(default=0, repr_type="Rating", repr_kwargs={"fractions": 2, "size": "xl"})
    detail: str | None = Field(default=None, repr_type="Textarea", repr_kwargs={"n_cols": 1.0})


class Routine(BaseModel):
    """Routine model."""

    date: datetime.date
    food: Food | None = Field(
        default=None,
        title=dmc.Group(
            [
                DashIconify(icon="fluent:food-20-regular", height=20),
                dmc.Text("Food", fw="bold"),
            ],
            gap="xs",
        ),
        repr_kwargs={"render_type": "simple"},
    )
    exercise: Exercise | None = Field(
        default=None,
        title=dmc.Group(
            [
                DashIconify(icon="icon-park-outline:sport", height=20),
                dmc.Text("Exercise", fw="bold"),
            ],
            gap="xs",
        ),
        repr_kwargs={"render_type": "simple"},
    )
    mood: Mood | None = Field(
        default=None,
        title=dmc.Group(
            [
                DashIconify(icon="tabler:mood-smile", height=20),
                dmc.Text("Mood", fw="bold"),
            ],
            gap="xs",
        ),
        repr_kwargs={"render_type": "simple"},
    )
    sleep: Sleep | None = Field(
        default=None,
        title=dmc.Group(
            [
                DashIconify(icon="mingcute:sleep-line", height=20),
                dmc.Text("Sleep", fw="bold"),
            ],
            gap="xs",
        ),
        repr_kwargs={"render_type": "simple"},
    )
