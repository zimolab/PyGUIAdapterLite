import dataclasses
from abc import abstractmethod
from inspect import isclass
from tkinter import Frame, Widget
from typing import Any, TypeVar, Type, Optional, Union

from pyguiadapterlite.utils import _warning


class SetValueError(Exception):
    def __init__(self, raw_value: Any, msg: Optional[str]):
        super().__init__(msg)
        self.raw_value = raw_value


class GetValueError(Exception):
    def __init__(self, raw_value: Any, msg: Optional[str]):
        super().__init__(msg)
        self.raw_value = raw_value


class InvalidValue(object):
    def __init__(self, raw_value: Any, msg: Optional[str] = None, data: Any = None):
        self.raw_value = raw_value
        self.msg = msg
        self.data = data


class ColorFlashEffect(object):
    def __init__(
        self,
        target_widget: Optional[Widget],
        flash_color="red",
        duration=1000,
        flashes=3,
    ):
        self.flash_color = flash_color
        self.duration = duration
        self.flashes = flashes

        self._widget: Optional[Widget] = None
        self._original_bg: Optional[str] = None
        self._flash_count = 0

        self.set_target(target_widget)

    def set_target(self, widget: Optional[Widget]):
        self._widget = widget
        if not self._widget:
            self._original_bg = None
            return
        self._original_bg = widget.cget("background")

    def start(self):
        if not self._widget:
            _warning("target widget is not set, this effect will not take effect")
            return
        self._flash_count = 0
        self._flash()

    def _flash(self):
        if self._flash_count < self.flashes * 2:
            if self._flash_count % 2 == 0:
                self._widget.configure(background=self.flash_color)
            else:
                self._widget.configure(background=self._original_bg)

            self._flash_count += 1
            self._widget.after(self.duration // (self.flashes * 2), self._flash)
        else:
            self._widget.configure(background=self._original_bg)


@dataclasses.dataclass(frozen=True)
class BaseParameterWidgetConfig(object):
    """值控件配置基类"""

    default_value: Any = None
    label: str = ""
    description: str = ""
    group: str = ""

    # noinspection PyAbstractClass
    @classmethod
    @abstractmethod
    def target_widget_class(cls) -> Type["BaseParameterWidget"]:
        raise NotImplementedError()

    @classmethod
    def new(cls, **kwargs) -> "BaseParameterWidgetConfig":
        return cls(**kwargs)


_T = TypeVar("_T", bound=BaseParameterWidgetConfig)


class BaseParameterWidget(Frame):
    """所有参数控件（输入控件）类的基类"""

    ConfigClass: Type[BaseParameterWidgetConfig] = NotImplemented

    def __init__(self, parent: Widget, parameter_name: str, config: _T):
        super().__init__(parent)
        self._parameter_name = parameter_name
        self._config = config
        self._label = self._config.label or self._parameter_name
        self._description = self._config.description or ""

        self._invalid_value_effect = ColorFlashEffect(self, "red", 800, 3)

    @property
    def parameter_name(self) -> str:
        return self._parameter_name

    @property
    def config(self) -> _T:
        return self._config

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, value: str):
        self._label = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def invalid_value_effect(self) -> ColorFlashEffect:
        return self._invalid_value_effect

    # noinspection PyAbstractClass
    @abstractmethod
    def get_value(self) -> Union[Any, InvalidValue]:
        """获取控件的值"""
        pass

    # noinspection PyAbstractClass
    @abstractmethod
    def set_value(self, value: Any) -> Union[Any, InvalidValue]:
        """设置控件的值"""
        pass

    # noinspection PyAbstractClass
    @abstractmethod
    def build(self) -> "BaseParameterWidget":
        pass

    @classmethod
    def new(
        cls,
        parent: Widget,
        parameter_name: str,
        config: _T,
    ):
        return cls(parent, parameter_name, config).build()

    def start_invalid_value_effect(self):
        self._invalid_value_effect.start()


def is_parameter_widget_class(o: Any) -> bool:
    return o is not None and isclass(o) and issubclass(o, BaseParameterWidget)
