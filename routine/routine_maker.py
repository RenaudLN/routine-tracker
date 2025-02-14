from datetime import date
from typing import Annotated, ClassVar, Literal, get_args

from pydantic import BaseModel, Field, create_model
from slugify import slugify

CATEGORIES = [
    "Exercise",
    "Mood",
    "Food",
    "Sleep",
    "Pain",
]


class FieldModel(BaseModel):
    type_: str = "string"
    name: str = Field()
    # repr_kwargs: dict[str, str] = Field(title="Representation options", default_factory=dict)
    # pydantic_kwargs: dict[str, str] = Field(title="Pydantic field options", default_factory=dict)

    annotation: ClassVar[type | None] = None
    default_repr: ClassVar[dict | None] = None
    label: ClassVar[str]

    def get_annotation(self):
        if self.annotation is not None:
            return self.annotation
        raise NotImplementedError(f"Annotation not implemented for {self.type_}")

    def get_repr_type(self):
        return (self.default_repr or {}).get("repr_type")

    def get_repr_kwargs(self):
        return (self.default_repr or {}).get("repr_kwargs", {})

    def to_dynamic_field(self) -> tuple[type, ...]:
        annotation = self.get_annotation()
        default = None
        json_schema_extra = {}
        if repr_type := self.get_repr_type():
            json_schema_extra["repr_type"] = repr_type
        if repr_kwargs := self.get_repr_kwargs():
            json_schema_extra["repr_kwargs"] = repr_kwargs
        return (
            annotation | None,
            Field(default=default, title=self.name, json_schema_extra=json_schema_extra),
        )

    @property
    def slug(self):
        return slugify(self.name).replace("-", "_")

    def __repr__(self):
        return f"{self.type_}({self['name']})"

    def __str__(self):
        return str(self["name"])


class StringFieldModel(FieldModel):
    type_: Literal["string"] = "string"

    label = "Text"
    annotation = str


class TextareaFieldModel(FieldModel):
    type_: Literal["textarea"] = "textarea"

    label = "Long Text"
    annotation = str
    default_repr = {"repr_type": "Textarea"}


class NumberFieldModel(FieldModel):
    type_: Literal["number"] = "number"
    decimal: bool = False

    label = "Number"
    default_repr = {"repr_kwargs": {"decimalScale": 0}}

    def get_annotation(self):
        return int if not self.decimal else float

    def get_repr_kwargs(self):
        return {"decimalScale": 0 if not self.decimal else None}


class RatingFieldModel(FieldModel):
    type_: Literal["rating"] = "rating"

    label = "Rating"
    annotation = float
    default_repr = {"repr_type": "Rating"}


class DateFieldModel(FieldModel):
    type_: Literal["date"] = "date"

    label = "Date"
    annotation = date


class SelectFieldModel(FieldModel):
    type_: Literal["select"] = "select"
    options: list[str] = Field(json_schema_extra={"repr_type": "Tags"})

    label = "Select"

    def get_annotation(self):
        return Literal[tuple(self.options)]

    @property
    def use_radio(self):
        return len(self.options) <= 3  # noqa: PLR2004

    def get_repr_type(self):
        return "RadioItems" if self.use_radio else "Select"

    def get_repr_kwargs(self):
        return {"orientation": "horizontal"} if self.use_radio else {}


class MultiSelectFieldModel(FieldModel):
    type_: Literal["multiselect"] = "multiselect"
    options: list[str] = Field(json_schema_extra={"repr_type": "Tags"})

    label = "Multi-Select"

    def get_annotation(self):
        return Literal[tuple(self.options)]

    @property
    def use_checklist(self):
        return len(self.options) <= 4  # noqa: PLR2004

    def get_repr_type(self):
        return "Checklist" if self.use_checklist else "MultiSelect"

    def get_repr_kwargs(self):
        return {"orientation": "horizontal"} if self.use_checklist else {}


FieldModelUnion = Annotated[
    StringFieldModel
    | TextareaFieldModel
    | NumberFieldModel
    | RatingFieldModel
    | DateFieldModel
    | SelectFieldModel
    | MultiSelectFieldModel,
    Field(discriminator="type_"),
]


class ListFieldModel(FieldModel):
    type_: Literal["list"] = "list"
    fields: list[FieldModelUnion] = Field(default_factory=list)

    label = "List"

    def get_annotation(self):
        submodel = create_model(
            f"{self.slug.title()}_", **{field.slug: field.to_dynamic_field() for field in self.fields}
        )
        return list[submodel]


AllFieldModelUnion = Annotated[
    StringFieldModel
    | TextareaFieldModel
    | NumberFieldModel
    | RatingFieldModel
    | DateFieldModel
    | SelectFieldModel
    | MultiSelectFieldModel
    | ListFieldModel,
    Field(discriminator="type_"),
]


field_options = [
    {
        "label": f.label,
        "value": get_args(f.model_fields["type_"].annotation)[0],
    }
    for f in get_args(get_args(AllFieldModelUnion)[0])
]


class RoutineBlock(BaseModel):
    category: str = Field(
        json_schema_extra={
            "repr_type": "Tags",
            "repr_kwargs": {"maxTags": 1, "data": CATEGORIES},
        },
    )
    fields: list[AllFieldModelUnion] = Field(default_factory=list)


class RoutineMaker(BaseModel):
    blocks: list[RoutineBlock] = Field(default_factory=list)

    def to_model(self):
        try:
            return create_model("Custom_", **{field.slug: field.to_dynamic_field() for field in self.fields})
        except Exception as exc:
            import traceback

            traceback.print_exc()
            raise exc
