import dataclasses
from tkinter import Widget, Scale
from typing import Type, Any, Optional, Union

from pyguiadapterlite.components.valuewidget import (
    BaseParameterWidget,
    BaseParameterWidgetConfig,
    GetValueError,
    InvalidValue,
    SetValueError,
)
from pyguiadapterlite.utils import _error

MIN_VALUE = 0.0
MAX_VALUE = 100.0
DEFAULT_STEP = 0.5
DEFAULT_VALUE = 0.0
DEFAULT_DIGITS = 0
DEFAULT_TICK_INTERVAL = 0


@dataclasses.dataclass(frozen=True)
class ScaleFloatValue(BaseParameterWidgetConfig):
    default_value: float = DEFAULT_VALUE
    min_value: float = MIN_VALUE
    max_value: float = MAX_VALUE
    step: float = DEFAULT_STEP
    digits: int = DEFAULT_DIGITS
    show_value: bool = True
    tick_interval: float = DEFAULT_TICK_INTERVAL

    def __post_init__(self):
        # 验证参数合理性
        if self.min_value >= self.max_value:
            raise ValueError("min_value must be less than max_value")
        if self.step <= 0:
            raise ValueError("step must be positive")
        if not (self.min_value <= self.default_value <= self.max_value):
            raise ValueError("default_value must be between min_value and max_value")

    @classmethod
    def target_widget_class(cls) -> Type["ScaleFloatValueWidget"]:
        return ScaleFloatValueWidget


class FloatScale(Scale):
    def __init__(self, parent: "ScaleFloatValueWidget", **kwargs):
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
    def value(self) -> Union[float, InvalidValue]:
        try:
            return float(self.get())
        except (ValueError, TypeError) as e:
            current_value = self.get()
            raise GetValueError(
                raw_value=current_value, msg=f"invalid float value `{current_value}`"
            ) from e

    @value.setter
    def value(self, value: float) -> None:
        config = self._parent.config

        try:
            float_value = float(value)
            # 检查是否在范围内
            if not (config.min_value <= float_value <= config.max_value):
                raise SetValueError(
                    raw_value=value,
                    msg=f"out of range [{config.min_value}, {config.max_value}]",
                )
            self.set(float_value)
        except (ValueError, TypeError) as e:
            raise SetValueError(
                raw_value=value, msg=f"invalid float value `{value}`"
            ) from e


class ScaleFloatValueWidget(BaseParameterWidget):
    ConfigClass = ScaleFloatValue

    def __init__(self, parent: Widget, parameter_name: str, config: ScaleFloatValue):
        super().__init__(parent, parameter_name, config)

        self._build_flag = False
        self._scale: Optional[FloatScale] = None

    @property
    def config(self) -> ScaleFloatValue:
        return super().config

    def get_value(self) -> Union[float, InvalidValue]:
        if not self._scale:
            raise RuntimeError("scale not created yet")
        try:
            return self._scale.value
        except GetValueError as e:
            self.on_parameter_error(self._parameter_name, e)
            return InvalidValue(raw_value=e.raw_value, exception=e)

    def set_value(self, value: Any) -> Union[float, InvalidValue]:
        if not self._scale:
            raise RuntimeError("scale not created yet")
        try:
            self._scale.value = value
            return value
        except SetValueError as e:
            self.on_parameter_error(self._parameter_name, e)
            return InvalidValue(raw_value=e.raw_value, exception=e)

    def build(self) -> "ScaleFloatValueWidget":
        if self._build_flag:
            return self

        # 创建滑块
        self._scale = FloatScale(self)
        self._scale.pack(fill="x", expand=True)
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
