import sys

import pyguiadapterlite
from pyguiadapterlite import (
    FnExecuteWindow,
    Action,
    SettingsWindow,
    SettingsWindowConfig,
    Menu,
    GUIAdapter,
    uprint,
    FnExecuteWindowConfig,
    JsonSettingsBase,
)
from pyguiadapterlite.types import StringValue, IntValue, RangedIntValue

APP_SETTINGS_FILE = "settings.json"


class AppSettings(JsonSettingsBase):
    url = StringValue(label="Remote URL", default_value="https://www.example.com")
    port = IntValue(label="Port Number", default_value=8080)
    username = StringValue(label="Username", default_value="admin")
    password = StringValue(label="Password", default_value="", echo_char="*")
    timeout = RangedIntValue(
        label="Timeout", default_value=10, min_value=1, max_value=60
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def load_settings() -> AppSettings:
    try:
        return AppSettings.load(file_path=APP_SETTINGS_FILE, encoding="utf-8")
    except BaseException as e:
        print(f"Error loading settings: {e}", file=sys.stderr)
        return AppSettings()


def save_settings(settings: AppSettings):
    try:
        settings.save(file_path=APP_SETTINGS_FILE, encoding="utf-8")
    except BaseException as e:
        print(f"Error saving settings: {e}", file=sys.stderr)


app_settings = load_settings()


def my_app_function(request: str):
    # Here we can access the settings fields using dot notation
    uprint(f"Remote URL: {app_settings.url}")
    uprint(f"Port Number: {app_settings.port}")
    uprint(f"Username: {app_settings.username}")
    uprint(f"Password: {app_settings.password}")
    uprint(f"Timeout: {app_settings.timeout}")
    uprint(f"Request: {request}")


if __name__ == "__main__":

    def on_action_show_settings(window: FnExecuteWindow, action: Action):
        _ = action  # Unused
        window.show_sub_window(
            SettingsWindow,
            settings=app_settings,
            modal=True,
            config=SettingsWindowConfig(
                title="Application Settings",
                content_title="Connection Options",
                confirm_button_text="Save Changes",
                cancel_button_text="Discard Changes",
                allow_restore_defaults=True,
                restore_defaults_button_text="Restore Defaults",
            ),
        )
        # save the settings here
        save_settings(app_settings)

    file_menu = Menu(
        title="File",
        actions=[Action(text="Settings", on_triggered=on_action_show_settings)],
    )

    pyguiadapterlite.set_locale_code("en_US")  # set language

    adapter = GUIAdapter(dpi_aware=True)  # enable high DPI support
    adapter.add(
        my_app_function,
        window_menus=[file_menu],
        window_config=FnExecuteWindowConfig(
            title="My App",  # set the title of the window
            print_function_result=False,  # don't print the result of the function to the console of the window
            show_function_result=False,  # don't show the result of the function in a message box
        ),
    )
    adapter.run()
    # app exited here
    # save the settings here
    save_settings(app_settings)
