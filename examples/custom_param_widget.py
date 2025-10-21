import dataclasses
from tkinter import Widget
from tkinter.ttk import Spinbox
from typing import Type, Any, Union, Optional

from pyguiadapterlite import uprint, GUIAdapter, ParameterWidgetFactory
from pyguiadapterlite.components.valuewidget import (
    BaseParameterWidgetConfig,
    BaseParameterWidget,
    InvalidValue,
)


class Point2D(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


@dataclasses.dataclass(frozen=True)
class Point2DValue(BaseParameterWidgetConfig):
    default_value: Point2D = dataclasses.field(default_factory=lambda: Point2D(0, 0))
    max_x: int = 100
    max_y: int = 100
    min_x: int = -100
    min_y: int = -100
    x_step: int = 1
    y_step: int = 1

    @classmethod
    def target_widget_class(cls) -> Type["BaseParameterWidget"]:
        return Point2DValueWidget


class Point2DValueWidget(BaseParameterWidget):

    ConfigClass = Point2DValue

    def __init__(self, parent: Widget, parameter_name: str, config: Point2DValue):
        self._x_spinbox: Optional[Spinbox] = None
        self._y_spinbox: Optional[Spinbox] = None
        self._is_build = False

        super().__init__(parent, parameter_name, config)

    def get_value(self) -> Union[Point2D, InvalidValue]:
        raw_x = self._x_spinbox.get()
        raw_y = self._y_spinbox.get()
        try:
            x = int(raw_x)
            y = int(raw_y)
        except BaseException as e:
            return InvalidValue(
                raw_value=(raw_x, raw_y),
                msg="cannot convert x or y to an integer",
                exception=e,
            )
        config: Point2DValue = self.config
        if x < config.min_x or x > config.max_x:
            return InvalidValue(
                raw_value=(raw_x, raw_y),
                msg=f"x value should be between {config.min_x} and {config.max_x}",
            )
        if y < config.min_y or y > config.max_y:
            return InvalidValue(
                raw_value=(raw_x, raw_y),
                msg=f"y value should be between {config.min_y} and {config.max_y}",
            )
        return Point2D(x, y)

    def set_value(self, value: Any) -> Union[Point2D, InvalidValue]:
        if not isinstance(value, Point2D):
            return InvalidValue(
                raw_value=value,
                msg="value should be a Point2D object",
            )
        config: Point2DValue = self.config
        if value.x < config.min_x or value.x > config.max_x:
            return InvalidValue(
                raw_value=value,
                msg=f"x value should be between {config.min_x} and {config.max_x}",
            )
        if value.y < config.min_y or value.y > config.max_y:
            return InvalidValue(
                raw_value=value,
                msg=f"y value should be between {config.min_y} and {config.max_y}",
            )
        self._x_spinbox.set(value.x)
        self._y_spinbox.set(value.y)
        return value

    def build(self) -> "BaseParameterWidget":
        if self._is_build:
            return self
        config: Point2DValue = self.config
        self._x_spinbox = Spinbox(
            self,
            from_=config.min_x,
            to=config.max_x,
            increment=config.x_step,
        )
        self._y_spinbox = Spinbox(
            self,
            from_=config.min_y,
            to=config.max_y,
            increment=config.y_step,
        )
        self._x_spinbox.pack(side="left", padx=5)
        self._y_spinbox.pack(side="left", padx=5)
        if config.default_value is not None:
            self._x_spinbox.set(config.default_value.x)
            self._y_spinbox.set(config.default_value.y)
        self._is_build = True
        return self


def test_point2d(point1: Point2D, point2: Point2D = Point2D(50, 60)):
    uprint(f"point1:({point1.x},{point1.y}), type: {type(point1)}")
    uprint(f"point2:({point2.x},{point2.y}), type: {type(point2)}")


if __name__ == "__main__":
    ParameterWidgetFactory.register(Point2D, Point2DValueWidget)
    adapter = GUIAdapter()
    adapter.add(
        test_point2d,
        point1=Point2DValue(
            default_value=Point2D(10, 20),
            min_x=0,
            max_x=100,
            min_y=0,
            max_y=100,
            x_step=10,
            y_step=10,
        ),
    )
    adapter.run()
