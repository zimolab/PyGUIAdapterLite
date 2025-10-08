import dataclasses
from tkinter import Widget
from tkinter.ttk import Scale, Label, Frame
from typing import Type, Any, Optional, Union

from pyguiadapterlite.components.valuewidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
    GetValueError,
    InvalidValue,
    SetValueError,
)
from pyguiadapterlite.utils import _error

MAX_VALUE = 100
MIN_VALUE = 0


@dataclasses.dataclass(frozen=True)
class ScaleIntValue(BaseParameterWidgetConfig):
    default_value: int = 0
    min_value: int = MIN_VALUE
    max_value: int = MAX_VALUE
    step: int = 1
    show_value: bool = True
    tick_interval: int = 0

    @classmethod
    def target_widget_class(cls) -> Type["ScaleIntValueWidget"]:
        return ScaleIntValueWidget


class IntScale(Scale):
    def __init__(self, parent: Widget, value_widget: "ScaleIntValueWidget", **kwargs):
        super().__init__(parent, **kwargs)
        self.config(
            from_=value_widget.config.min_value,
            to=value_widget.config.max_value,
            orient="horizontal",
        )
        self._parent = parent
        self._value_widget = value_widget

    @property
    def value(self) -> Union[int, InvalidValue]:
        current_value = self.get()
        try:
            val = int(current_value)
        except ValueError as e:
            raise GetValueError(
                raw_value=current_value, msg=f"cannot convert to int"
            ) from e
        if (
            val < self._value_widget.config.min_value
            or val > self._value_widget.config.max_value
        ):
            raise GetValueError(
                raw_value=current_value,
                msg=f"out of range [{self._value_widget.config.min_value}, {self._value_widget.config.max_value}]",
            )
        return val

    @value.setter
    def value(self, value: int) -> Optional[InvalidValue]:
        raw_value = value
        try:
            value = int(raw_value)
        except ValueError as e:
            raise SetValueError(
                raw_value=raw_value, msg=f"cannot convert to int"
            ) from e
        if (
            value < self._value_widget.config.min_value
            or value > self._value_widget.config.max_value
        ):
            raise SetValueError(
                raw_value=raw_value,
                msg=f"out of range [{self._value_widget.config.min_value}, {self._value_widget.config.max_value}]",
            )
        self.set(value)


class ScaleIntValueWidget(BaseParameterWidget):
    ConfigClass = ScaleIntValue

    def __init__(self, parent: Widget, parameter_name: str, config: ScaleIntValue):
        self._build_flag = False
        self._input_widget: Optional[IntScale] = None
        self._value_label: Optional[Label] = None
        self._frame: Optional[Frame] = None

        super().__init__(parent, parameter_name, config)

    @property
    def config(self) -> ScaleIntValue:
        return self._config

    def get_value(self) -> Union[int, InvalidValue]:
        if not self._input_widget:
            raise RuntimeError("input widget not created yet")
        try:
            return self._input_widget.value
        except GetValueError as e:
            self.on_parameter_error(self._parameter_name, e)
            return InvalidValue(raw_value=e.raw_value, exception=e)

    def set_value(self, value: Any) -> Union[int, InvalidValue]:
        if not self._input_widget:
            raise RuntimeError("input widget not created yet")
        try:
            self._input_widget.value = value
            return value
        except SetValueError as e:
            self.on_parameter_error(self._parameter_name, e)
            return InvalidValue(raw_value=e.raw_value, exception=e)

    def build(self) -> "ScaleIntValueWidget":
        if self._build_flag:
            return self
        self._frame = Frame(self)
        self._frame.pack(fill="both", expand=True, padx=1, pady=1)
        self._input_widget = IntScale(
            self._frame, value_widget=self, command=self.on_value_changed
        )
        self._input_widget.pack(side="left", fill="both", expand=True)
        self._input_widget.value = self._config.default_value
        if self._config.show_value:
            self._value_label = Label(self._frame, justify="center", anchor="center")
            self._value_label.pack(side="right", fill="x", expand=False)
            self.on_value_changed(None)
        self.invalid_value_effect.set_target(self)
        # noinspection PyTypeChecker

        self._build_flag = True
        return self

    def on_parameter_error(self, parameter_name: str, error: Any) -> None:
        if parameter_name == self._parameter_name:
            if isinstance(error, GetValueError):
                _error(
                    f"failed to get value from widget of parameter `{parameter_name}`: {error}"
                )
                self.start_invalid_value_effect()
                return

    def on_value_changed(self, value: Optional[int]) -> None:
        _ = value
        if self._value_label:
            self._value_label.config(text=str(self._input_widget.value))
