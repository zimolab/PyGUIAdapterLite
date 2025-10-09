import dataclasses
from tkinter import Widget, Scale
from tkinter import ttk
from tkinter.ttk import Label, Frame
from typing import Type, Any, Optional, Union

from pyguiadapterlite.components.valuewidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
    GetValueError,
    InvalidValue,
    SetValueError,
)
from pyguiadapterlite.utils import _error

MIN_VALUE = 0
MAX_VALUE = 100
DEFAULT_STEP = 1
DEFAULT_VALUE = 0
DEFAULT_DIGITS = 0
DEFAULT_TICK_INTERVAL = 10


@dataclasses.dataclass(frozen=True)
class ScaleIntValue(BaseParameterWidgetConfig):
    default_value: int = 0
    min_value: int = MIN_VALUE
    max_value: int = MAX_VALUE
    show_value: bool = True
    cursor: str = "hand2"

    def __post_init__(self):
        # 验证参数合理性
        if self.min_value >= self.max_value:
            raise ValueError("min_value must be less than max_value")

        if not (self.min_value <= self.default_value <= self.max_value):
            raise ValueError("default_value must be between min_value and max_value")

    @classmethod
    def target_widget_class(cls) -> Type["ScaleIntValueWidget"]:
        return ScaleIntValueWidget


class IntScale(ttk.Scale):
    def __init__(self, parent: Widget, value_widget: "ScaleIntValueWidget", **kwargs):
        super().__init__(parent, **kwargs)
        self.config(
            from_=value_widget.config.min_value,
            to=value_widget.config.max_value,
            orient="horizontal",
            cursor=value_widget.config.cursor,
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


@dataclasses.dataclass(frozen=True)
class ScaleIntValue_tk(ScaleIntValue):
    step: int = DEFAULT_STEP
    digits: int = DEFAULT_DIGITS
    tick_interval: int = DEFAULT_TICK_INTERVAL

    def __post_init__(self):
        super().__post_init__()
        if self.step <= 0:
            raise ValueError("step must be positive")
        if self.digits < 0:
            raise ValueError("digits must be positive")

    @classmethod
    def target_widget_class(cls) -> Type["ScaleIntValueWidget_tk"]:
        return ScaleIntValueWidget_tk


class IntScale_tk(Scale):
    def __init__(self, parent: "ScaleIntValueWidget_tk", **kwargs):
        self._parent = parent
        config = parent.config

        # 设置Scale的范围和分辨率
        super().__init__(
            parent,
            from_=config.min_value,
            to=config.max_value,
            resolution=config.step,
            orient="horizontal",
            digits=config.digits,
            showvalue=config.show_value,
            tickinterval=config.tick_interval,
            **kwargs,
        )

        # 初始值
        self.set(config.default_value)

    @property
    def value(self) -> Union[int, InvalidValue]:
        try:
            return int(self.get())
        except (ValueError, TypeError) as e:
            current_value = self.get()
            raise GetValueError(
                raw_value=current_value, msg=f"invalid int value `{current_value}`"
            ) from e

    @value.setter
    def value(self, value: int) -> None:
        config = self._parent.config
        try:
            int_value = int(value)
            # 检查是否在范围内
            if not (config.min_value <= int_value <= config.max_value):
                raise SetValueError(
                    raw_value=value,
                    msg=f"out of range [{config.min_value}, {config.max_value}]",
                )
            self.set(int_value)
        except (ValueError, TypeError) as e:
            raise SetValueError(
                raw_value=value, msg=f"invalid int value `{value}`"
            ) from e


class ScaleIntValueWidget_tk(BaseParameterWidget):
    ConfigClass = ScaleIntValue_tk

    def __init__(self, parent: Widget, parameter_name: str, config: ScaleIntValue_tk):
        super().__init__(parent, parameter_name, config)

        self._build_flag = False
        self._scale: Optional[IntScale_tk] = None

    @property
    def config(self) -> ScaleIntValue_tk:
        return super().config

    def get_value(self) -> Union[int, InvalidValue]:
        if not self._scale:
            raise RuntimeError("scale not created yet")
        try:
            return self._scale.value
        except GetValueError as e:
            self.on_parameter_error(self._parameter_name, e)
            return InvalidValue(raw_value=e.raw_value, exception=e)

    def set_value(self, value: Any) -> Union[int, InvalidValue]:
        if not self._scale:
            raise RuntimeError("scale not created yet")
        try:
            self._scale.value = value
            return value
        except SetValueError as e:
            self.on_parameter_error(self._parameter_name, e)
            return InvalidValue(raw_value=e.raw_value, exception=e)

    def build(self) -> "ScaleIntValueWidget_tk":
        if self._build_flag:
            return self

        # 创建滑块
        self._scale = IntScale_tk(self)
        self._scale.pack(fill="x", expand=True, padx=1, pady=1)
        # 设置初始值
        self._scale.value = self._config.default_value
        # 设置无效值效果目标
        self.color_flash_effect.set_target(self)
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
        self.color_flash_effect.set_target(self)
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
