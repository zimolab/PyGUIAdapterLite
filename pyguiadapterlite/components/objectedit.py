from tkinter import Widget
from tkinter.ttk import Frame
from typing import Dict, Any, Union

from pyguiadapterlite.components.scrollarea import ParameterWidgetArea
from pyguiadapterlite.components.valuewidget import (
    BaseParameterWidgetConfig,
    InvalidValue,
)
from pyguiadapterlite.utils import _warning
from pyguiadapterlite.windows.basewindow import BaseWindow


class ObjectWidgetArea(ParameterWidgetArea):
    def __init__(self, parent: "ObjectFrame", window: BaseWindow):
        super().__init__(parent, window=window)


class ObjectFrame(Frame):
    def __init__(
        self,
        parent: Union[Widget],
        parent_window: BaseWindow,
        object_schema: Dict[str, BaseParameterWidgetConfig],
    ):
        self._parent_widget = parent or parent_window.parent
        self._parent_window = parent_window
        self._object_schema = object_schema
        super().__init__(self._parent_widget)

        self._object_area = self._create_object_area()
        self._object_area.pack(side="top", fill="both", padx=5, pady=5, expand=True)

    def _create_object_area(self) -> ObjectWidgetArea:
        object_area = ObjectWidgetArea(self, self._parent_window)
        for key, config in self._object_schema.items():
            object_area.add_parameter(key, config)
        return object_area

    def update_object(
        self, new_object: Dict[str, Any], ignore_not_exist: bool = True
    ) -> Dict[str, Union[Any, InvalidValue]]:
        return self._object_area.update_parameter_values(new_object, ignore_not_exist)

    def get_object(self) -> Dict[str, Union[Any, InvalidValue]]:
        return self._object_area.get_parameter_values()

    def set_value(self, key: str, value: Any) -> Union[Any, InvalidValue]:
        key_widget = self._object_area.get_parameter_widget(key)
        if not key_widget:
            return InvalidValue(f"widget for key `{key}` not found.")
        return key_widget.set_value(value)

    def get_value(self, key: str) -> Union[Any, InvalidValue]:
        key_widget = self._object_area.get_parameter_widget(key)
        if not key_widget:
            return InvalidValue(f"widget for key `{key}` not found.")
        return key_widget.get_value()

    def has_key(self, key: str) -> bool:
        return self._object_area.has_parameter(key)

    def show_error_effect(self, key: str):
        key_widget = self._object_area.get_parameter_widget(key)
        if not key_widget:
            _warning(f"widget for key `{key}` not found.")
            return
        key_widget.start_invalid_value_effect()
