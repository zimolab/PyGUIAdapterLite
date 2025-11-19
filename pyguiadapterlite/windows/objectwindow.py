import dataclasses
from tkinter import Tk, Toplevel
from tkinter.ttk import Button, Frame, LabelFrame
from typing import Union, Optional, Any, cast, Dict, Callable

from pyguiadapterlite import BaseParameterWidgetConfig
from pyguiadapterlite._messages import (
    MSG_OBJ_VALIDATION_WIN_TITLE,
    MSG_INVALID_KEYS_GROUP_TITLE,
    MSG_INVALID_KEY_LABEL_TEXT,
    MSG_INVALID_KEY_DETAIL_GROUP_TITLE,
    MSG_INVALID_KEY_DETAIL_TEMPLATE,
    MSG_OBJ_WIN_CONFIRM_BUTTON_TEXT,
    MSG_OBJ_WIN_CANCEL_BUTTON_TEXT,
    MSG_OBJ_WIN_CONTENT_TITLE,
    MSG_OBJ_WIN_TITLE,
)
from pyguiadapterlite.components.common import get_default_widget_font
from pyguiadapterlite.components.objectedit import ObjectFrame
from pyguiadapterlite.components.valuewidget import InvalidValue
from pyguiadapterlite.core.fn import ExecuteStateListener
from pyguiadapterlite.windows.basewindow import BaseWindowConfig, BaseWindow
from pyguiadapterlite.windows.fnvalidationwindow import (
    ParameterValidationWindow,
    ParameterValidationWindowConfig,
)


@dataclasses.dataclass(frozen=True)
class ObjectValidationWindowConfig(ParameterValidationWindowConfig):
    title: str = MSG_OBJ_VALIDATION_WIN_TITLE
    invalid_params_group_title: str = MSG_INVALID_KEYS_GROUP_TITLE
    invalid_params_label_text: str = MSG_INVALID_KEY_LABEL_TEXT
    description_group_title: str = MSG_INVALID_KEY_DETAIL_GROUP_TITLE
    invalid_param_detail_template: str = MSG_INVALID_KEY_DETAIL_TEMPLATE
    size: tuple = (400, 450)
    font: tuple = dataclasses.field(default_factory=get_default_widget_font)
    bell: bool = True


@dataclasses.dataclass(frozen=True)
class ObjectWindowConfig(BaseWindowConfig):
    title: str = MSG_OBJ_WIN_TITLE

    size: tuple = (500, 600)

    object_schema: Dict[str, BaseParameterWidgetConfig] = dataclasses.field(
        default_factory=dict
    )

    initial_object: Optional[Dict[str, Any]] = None

    check_initial_object: bool = True

    content_title: Optional[str] = MSG_OBJ_WIN_CONTENT_TITLE

    confirm_button_text: str = MSG_OBJ_WIN_CONFIRM_BUTTON_TEXT

    cancel_button_text: str = MSG_OBJ_WIN_CANCEL_BUTTON_TEXT

    font: tuple = dataclasses.field(default_factory=get_default_widget_font)

    after_window_create_callback: Optional[Callable[["ObjectWindow"], None]] = None
    """窗口创建后回调此函数。"""

    before_window_close_callback: Optional[Callable[["ObjectWindow"], bool]] = None
    """窗口关闭前回调此函数，如果返回`True`则表示允许关闭窗口，否则不允许关闭窗口。"""

    on_confirm_callback: Optional[Callable[["ObjectWindow", Dict[str, Any]], None]] = (
        None
    )

    on_cancel_callback: Optional[Callable[["ObjectWindow"], None]] = None


class BottomArea(Frame):
    def __init__(self, parent_window: "ObjectWindow", **kwargs):

        self._parent_window = parent_window
        self._config = parent_window.config

        self._confirm_button: Optional[Button] = None
        self._cancel_button: Optional[Button] = None

        super().__init__(parent_window.parent, **kwargs)

        self._create_controls()

    def _create_controls(self):
        self._confirm_button = Button(
            self,
            text=self._config.confirm_button_text,
            command=self._parent_window.on_confirm,
        )
        self._cancel_button = Button(
            self,
            text=self._config.cancel_button_text,
            command=self._parent_window.on_cancel,
        )

        self._cancel_button.pack(side="right", padx=5, pady=5)
        self._confirm_button.pack(side="right", padx=5, pady=5)


class ObjectWindow(BaseWindow, ExecuteStateListener):
    def __init__(
        self,
        parent: Union[Tk, Toplevel],
        config: Optional[ObjectWindowConfig] = None,
    ):
        config = config or ObjectWindowConfig()

        self._object_schema = config.object_schema
        self._initial_object = config.initial_object or {}

        self._main_area: Optional[ObjectFrame] = None
        self._bottom_area: Optional[BottomArea] = None
        self._validation_win_parent: Optional[Toplevel] = None
        self._validation_win: Optional[ParameterValidationWindow] = None

        super().__init__(parent, config)

        if config.after_window_create_callback:
            config.after_window_create_callback(self)

        if self._initial_object:
            self.update_object(
                self._initial_object.copy(),
                ignore_not_exist=True,
                check_invalid_values=config.check_initial_object,
            )

    @property
    def config(self) -> ObjectWindowConfig:
        return cast(ObjectWindowConfig, super().config)

    @property
    def main_area(self) -> ObjectFrame:
        return self._main_area

    @property
    def bottom_area(self) -> BottomArea:
        return self._bottom_area

    def create_main_area(self) -> Any:
        main_area_container = LabelFrame(
            self.parent, text=self.config.content_title or self.config.title
        )
        main_area_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        self._main_area = ObjectFrame(
            main_area_container, self, self.config.object_schema
        )
        self._main_area.pack(side="top", fill="both", expand=True, padx=5)

    def create_bottom_area(self) -> Any:
        bottom_area = BottomArea(self)
        bottom_area.pack(side="bottom", fill="x", padx=5, pady=(5, 2), expand=False)
        self._bottom_area = bottom_area

    def after(self, delay: int, func, *args):
        return self.parent.after(delay, func, *args)

    def close(self):
        self.on_close()

    def on_close(self):
        if self.config.before_window_close_callback:
            if not self.config.before_window_close_callback(self):
                return False

        self.close_validation_win()
        return super().on_close()

    def on_confirm(self):
        self.close_validation_win()
        current_object = self.get_object()
        callback = self.config.on_confirm_callback
        close_wind = True
        if callback:
            close_wind = callback(self, current_object)

        if (
            self._initial_object
            and current_object
            and self._initial_object != current_object
        ):
            self._initial_object.update(current_object)

        if close_wind:
            self.close()

    def on_cancel(self):
        self.close_validation_win()
        callback = self.config.on_cancel_callback
        if callback:
            callback(self)
        self.close()

    def get_object(self) -> Dict[str, Union[Any, InvalidValue]]:
        return self._main_area.get_object()

    def update_object(
        self,
        new_object: Dict[str, Any],
        ignore_not_exist: bool = True,
        check_invalid_values: bool = False,
    ) -> Dict[str, Union[Any, InvalidValue]]:
        ret = self._main_area.update_object(new_object, ignore_not_exist)
        if check_invalid_values:
            self.close_validation_win()
            self.check_invalid_values(result=ret)
            return ret
        return ret

    def check_invalid_values(self, result: Dict[str, Union[Any, InvalidValue]]):
        invalid = {}
        for key, value in result.items():
            if isinstance(value, InvalidValue):
                invalid_msg = value.msg or value.exception
                label = self._get_label_for_key(key)
                invalid[key] = (label, str(invalid_msg))
        if not invalid:
            return True

        validation_wind_config = ObjectValidationWindowConfig(font=self.config.font)

        self.show_validation_window(invalid, validation_wind_config)
        return False

    def show_validation_window(
        self,
        obj: Dict[Any, Any],
        validation_wind_config: ObjectValidationWindowConfig,
    ):
        self.close_validation_win()
        self._validation_win_parent = Toplevel(self._parent)
        self._validation_win = ParameterValidationWindow(
            self._validation_win_parent,
            invalid_params=obj,
            config=validation_wind_config,
        )
        self._validation_win.set_on_close_handler(self._on_validation_win_close)
        self._validation_win.set_item_clicked_handler(
            self._on_validation_win_item_clicked
        )

    def _get_label_for_key(self, key: str) -> str:
        for key1, config in self._object_schema.items():
            if key == key1:
                return config.label or key
        return key

    def close_validation_win(self):
        if self._validation_win:
            self._validation_win.on_close()

    def _on_validation_win_close(self):
        self._validation_win = None
        self._validation_win_parent = None

    def _on_validation_win_item_clicked(self, key: str):
        self._main_area.show_error_effect(key)
