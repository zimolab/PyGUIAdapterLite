import dataclasses
import tkinter as tk

from tkinter import Widget, Entry
from typing import Type, Any, Optional, Union

from pyguiadapterlite.components.utils import _error
from pyguiadapterlite.components.valuewidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
    GetValueError,
    InvalidValue,
    SetValueError,
)


@dataclasses.dataclass(frozen=True)
class IntValue(BaseParameterWidgetConfig):
    default_value: int = 0
    invalid_fallback_value: int = 0

    entry_configs: Optional[dict] = None

    @classmethod
    def target_widget_class(cls) -> Type["IntValueWidget"]:
        return IntValueWidget


class IntEntry(Entry):
    def __init__(self, master: Widget, invalid_fallback_value: int = 0, **kwargs):
        super().__init__(master, **kwargs)

        self.invalid_fallback_value = invalid_fallback_value

        self._validate_command = self.register(self.validate_input)
        self.configure(
            validate="key",
            validatecommand=(self._validate_command, "%P"),
        )
        self.bind("<FocusOut>", self.on_focus_out)

    @staticmethod
    def validate_input(value: str) -> bool:
        value = value.strip()
        if value == "" or value == "-":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def on_focus_out(self, event):
        _ = event
        value = self.get().strip()
        if value == "" or value == "-":
            self.delete(0, tk.END)
            self.insert(tk.END, str(self.invalid_fallback_value))

    @property
    def value(self) -> Union[int, InvalidValue]:
        current_value = self.get().strip()
        try:
            return int(self.get().strip())
        except ValueError as e:
            raise GetValueError(
                raw_value=current_value, msg=f"invalid int value `{current_value}`"
            ) from e

    @value.setter
    def value(self, value: int) -> Optional[InvalidValue]:
        raw_value = value
        try:
            value = int(raw_value)
        except ValueError as e:
            raise SetValueError(
                raw_value=raw_value, msg=f"invalid int value `{value}`"
            ) from e
        self.delete(0, tk.END)
        self.insert(tk.END, str(value))


class IntValueWidget(BaseParameterWidget):
    ConfigClass = IntValue

    def __init__(self, parent: Widget, parameter_name: str, config: IntValue):
        super().__init__(parent, parameter_name, config)

        self._build_flag = False
        self._input_entry: Optional[IntEntry] = None

    def get_value(self) -> Union[int, InvalidValue]:
        if not self._input_entry:
            raise RuntimeError("input entry not created yet")
        try:
            return self._input_entry.value
        except GetValueError as e:
            self.on_parameter_error(self._parameter_name, e)
            return InvalidValue(raw_value=e.raw_value, data=e)

    def set_value(self, value: Any) -> Union[int, InvalidValue]:
        if not self._input_entry:
            raise RuntimeError("input entry not created yet")
        try:
            self._input_entry.value = value
            return value
        except SetValueError as e:
            self.on_parameter_error(self._parameter_name, e)
            return InvalidValue(raw_value=e.raw_value, data=e)

    def build(self) -> "IntValueWidget":
        if self._build_flag:
            return self
        self._build_flag = True
        self._input_entry = IntEntry(
            self,
            invalid_fallback_value=self._config.invalid_fallback_value,
            **(self._config.entry_configs or {}),
        )
        self.invalid_value_effect.set_target(self._input_entry)
        # noinspection PyTypeChecker
        self._input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._input_entry.value = self._config.default_value

        return self

    def on_parameter_error(self, parameter_name: str, error: Any) -> None:
        if parameter_name == self._parameter_name:
            if isinstance(error, GetValueError):
                _error(
                    f"failed to get value from widget of parameter `{parameter_name}`: {error}"
                )
                self.start_invalid_value_effect()
                return
