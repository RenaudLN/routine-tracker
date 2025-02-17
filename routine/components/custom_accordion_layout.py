from typing import Literal

import dash_mantine_components as dmc
from dash.development.base_component import Component
from dash_pydantic_form import FormLayout


class CustomAccordionLayout(FormLayout):
    """Custom accordion layout."""

    layout: Literal["custom_accordion"] = "custom_accordion"

    def render(  # noqa: PLR0913
        self,
        *,
        field_inputs: dict[str, Component],
        aio_id: str,  # noqa: ARG002
        form_id: str,  # noqa: ARG002
        path: str,  # noqa: ARG002
        read_only: bool,  # noqa: ARG002
        form_cols: int,  # noqa: ARG002
    ):
        """Render the custom accordion."""
        return [
            self.grid(
                ([field_inputs["date"]] if "date" in field_inputs else [])
                + ([field_inputs["routine_ref"]] if "routine_ref" in field_inputs else [])
                + [
                    dmc.Accordion(
                        [
                            dmc.AccordionItem(
                                [
                                    dmc.AccordionControl(v.children.children[0]),
                                    dmc.AccordionPanel(self.grid(v.children.children[1:])),
                                ],
                                value=k,
                            )
                            for k, v in field_inputs.items()
                            if k not in ["date", "routine_ref"]
                        ],
                        value=None,
                    )
                ]
            )
        ]
