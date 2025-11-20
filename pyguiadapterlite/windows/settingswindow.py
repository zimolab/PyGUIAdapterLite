import dataclasses
from dataclasses import field
from tkinter import Toplevel, Tk
from tkinter.ttk import Button
from typing import Dict, Union, Optional, Callable, cast

from pyguiadapterlite import BaseParameterWidgetConfig
from pyguiadapterlite._messages import messages
from pyguiadapterlite.components.settingsbase import SettingsBase
from pyguiadapterlite.windows.objectwindow import ObjectWindowConfig, ObjectWindow


@dataclasses.dataclass(frozen=True)
class SettingsWindowConfig(ObjectWindowConfig):
    title: str = field(default_factory=lambda: messages().MSG_SETTINGS_WIN_TITLE)
    content_title: Optional[str] = field(
        default_factory=lambda: messages().MSG_SETTINGS_WIN_CONTENT_TITLE
    )
    confirm_button_text: str = field(
        default_factory=lambda: messages().MSG_SETTINGS_WIN_CONFIRM_BUTTON_TEXT
    )
    cancel_button_text: str = field(
        default_factory=lambda: messages().MSG_SETTINGS_WIN_CANCEL_BUTTON_TEXT
    )

    allow_restore_defaults: bool = True
    restore_defaults_button_text: str = field(
        default_factory=lambda: messages().MSG_SETTINGS_WIN_RESTORE_DEFAULT_BUTTON_TEXT
    )
    restore_defaults_confirm_message: str = field(
        default_factory=lambda: messages().MSG_SETTINGS_WIN_RESTORE_DEFAULT_CONFIRM_MSG
    )

    # don't need to set the following fields
    # they will not take effect in SettingsWindow
    object_schema: Dict[str, BaseParameterWidgetConfig] = None
    on_confirm_callback: Callable = None
    on_cancel_callback: Callable = None
    initial_object: dict = None


SettingFields = Union[
    Dict[str, BaseParameterWidgetConfig],
    Callable[[SettingsBase], Dict[str, BaseParameterWidgetConfig]],
    None,
]


class SettingsWindow(ObjectWindow):
    def __init__(
        self,
        parent: Union[Tk, Toplevel],
        config: Optional[SettingsWindowConfig],
        settings: SettingsBase,
        setting_fields: SettingFields = lambda settings: settings.__class__.fields(),
        after_save_callback: Optional[Callable[[SettingsBase], None]] = None,
    ):
        config = config or SettingsWindowConfig()

        if setting_fields is None:
            object_schema = settings.__class__.fields()
        elif callable(setting_fields):
            object_schema = setting_fields(settings)
        elif isinstance(setting_fields, dict):
            object_schema = setting_fields
        else:
            raise TypeError("Invalid setting_fields type")

        settings_values = settings.values()

        config = dataclasses.replace(
            config, object_schema=object_schema, initial_object=settings_values
        )
        self._after_save_callback = after_save_callback
        self._settings = settings

        super().__init__(parent, config)

        if config.allow_restore_defaults:
            self._restore_defaults_button = Button(
                self._bottom_area,
                text=config.restore_defaults_button_text,
                command=self.on_restore_defaults,
            )
            self._restore_defaults_button.pack(side="left")

    def on_restore_defaults(self):
        if not self.config.allow_restore_defaults:
            return
        if not self.ask_yes_no(
            message=self.config.restore_defaults_confirm_message,
            parent=self.parent.winfo_toplevel(),
        ):
            return

        default_settings_values = self._settings.__class__.default_values()
        self.update_object(default_settings_values)

    def on_confirm(self):
        current_settings_values = self.get_object()
        all_valid = self.check_invalid_values(current_settings_values)
        if not all_valid:
            return
        self._settings.set_values(current_settings_values)
        self.close()
        if self._after_save_callback:
            self._after_save_callback(self._settings)

    def on_cancel(self):
        self.close()

    @property
    def config(self) -> SettingsWindowConfig:
        return cast(SettingsWindowConfig, super().config)
