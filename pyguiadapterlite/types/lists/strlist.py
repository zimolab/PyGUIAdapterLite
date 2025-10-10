import dataclasses
from tkinter import Widget
from tkinter.ttk import Button
from typing import Type, Optional, Literal, List

from pyguiadapterlite.components.dialog import StringInputDialog
from pyguiadapterlite.types.lists._common import (
    BaseStringListValue,
    BaseStringListValueWidget,
    BaseStringListBox,
)
from pyguiadapterlite.utils import show_warning


@dataclasses.dataclass(frozen=True)
class StringListValue(BaseStringListValue):

    add_button: bool = True
    add_button_text: str = "Add"
    add_method: Literal["append", "prepend"] = "append"

    strip: bool = False

    accept_empty: bool = True
    empty_string_message: str = "Empty string is not allowed"

    accept_duplicates: bool = True
    duplicate_message: str = "String already exists in the list"

    multi_selection_message: str = "Please select only one item to be edited"

    @classmethod
    def target_widget_class(cls) -> Type["StringListValueWidget"]:
        return StringListValueWidget


class StringListBox(BaseStringListBox):
    def __init__(self, parent: "StringListValueWidget", **kwargs):
        self._add_button: Optional[Button] = None
        self._config: StringListValue = parent.config

        super().__init__(parent, **kwargs)

    def on_edit(self, indexes: List[int]):
        if not indexes:
            show_warning(self._config.no_selection_message)
            return
        if len(indexes) > 1:
            show_warning(self._config.multi_selection_message)
            return
        index = indexes[0]
        current_value = self._listview.real.get(index)
        dialog = StringInputDialog(
            self,
            title="Edit",
            label_text="Edit",
            initial_value=str(current_value),
        )
        if dialog.is_cancelled():
            return
        new_value = dialog.result
        new_value = self._process_input(new_value)
        if new_value is None:
            return
        self._listview.real.set(index, new_value)

    def _process_input(self, input_str: str) -> Optional[str]:
        value = str(input_str)
        if self._config.strip:
            value = value.strip()

        if not self._config.accept_empty and value.strip() == "":
            show_warning(self._config.empty_string_message)
            return None

        if not self._config.accept_duplicates and self._listview.real.contains(value):
            show_warning(self._config.duplicate_message)
            return None

        return value

    def _on_add_item(self):
        input_dialog = StringInputDialog(self, "Add Item")
        if input_dialog.is_cancelled():
            return
        value = input_dialog.result
        if value is None:
            return

        value = self._process_input(value)
        if value is None:
            return

        if self._config.add_method == "append":
            self._listview.real.append(value)
        else:
            self._listview.real.prepend(value)

    def _create_buttons(self):
        super()._create_buttons()
        if self._config.add_button:
            self._add_button = Button(
                self.buttons_area,
                text=self._config.add_button_text,
                command=self._on_add_item,
            )
            self._add_button.pack(side="right", padx=2, pady=2)


class StringListValueWidget(BaseStringListValueWidget):
    ConfigClass = StringListValue

    def __init__(
        self,
        parent: Widget,
        parameter_name: str,
        config: StringListValue,
    ):
        super().__init__(StringListBox, parent, parameter_name, config)

    @property
    def config(self) -> StringListValue:
        return self._config
