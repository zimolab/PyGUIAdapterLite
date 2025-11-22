import sys
from typing import Union

import pyguiadapterlite
from pyguiadapterlite import (
    SettingsBase,
    FnExecuteWindow,
    Action,
    SettingsWindow,
    SettingsWindowConfig,
    Menu,
    GUIAdapter,
    uprint,
    FnExecuteWindowConfig,
)
from pyguiadapterlite.types import StringValue, IntValue, RangedIntValue


class AppSettings(SettingsBase):
    # Define the fields of the settings as the class attributes of the SettingsBase subclass
    url = StringValue(label="Remote URL", default_value="https://www.example.com")
    port = IntValue(label="Port Number", default_value=8080)
    username = StringValue(label="Username", default_value="admin")
    password = StringValue(label="Password", default_value="", echo_char="*")
    timeout = RangedIntValue(
        label="Timeout", default_value=10, min_value=1, max_value=60
    )

    def __init__(self, **kwargs):
        # Usually, you need to override __init__ method like this if we want to set the initial values of the fields
        # in this form:
        # AppSettings(url="https://www.example.com", port=8080, username="admin", password="")
        super().__init__(**kwargs)

    def serialize(self) -> Union[str, bytes]:
        # This method is used to serialize the settings to a string or bytes object, which can be saved to file or
        # sent over the network. Here we just return a json string of the settings fields.
        import json

        return json.dumps(
            self.values(),  # SettingsBase.values() returns a dictionary of the settings fields and values
            indent=4,
            ensure_ascii=False,
        )

    @classmethod
    def deserialize(cls, data: Union[str, bytes], **kwargs) -> "AppSettings":
        # This method is used to deserialize the settings from a string or bytes object
        try:
            import json

            values = json.loads(data, **kwargs)
            return cls(**values)
        except Exception as e:
            print(f"Error deserializing settings: {e}", file=sys.stderr)
            # If there is an error deserializing the settings,
            # return a new instance of AppSettings with default values
            return cls()


# Create an instance of AppSettings
# In real application, the settings instance may be initialized with values from a settings file,
# database or other sources. For example:

# try:
#     with open("settings.json", "r") as f:
#         settings = AppSettings.deserialize(f.read())
# except Exception as e:
#     print(f"Error loading settings: {e}", file=sys.stderr)
#     print("Using default settings.")
#     settings = AppSettings()

# Here we just create a new instance of AppSettings for simplicity.
settings = AppSettings(
    url="https://www.anotherexample.com",
    port=8080,
    username="tom",
    password="123456",
    timeout=15,
)


def my_app_function(request: str):
    # Here we can access the settings fields using dot notation
    uprint(f"Remote URL: {settings.url}")
    uprint(f"Port Number: {settings.port}")
    uprint(f"Username: {settings.username}")
    uprint(f"Password: {settings.password}")
    uprint(f"Timeout: {settings.timeout}")
    uprint(f"Request: {request}")


if __name__ == "__main__":

    # Create a menu to show the settings window
    def on_action_show_settings(window: FnExecuteWindow, action: Action):
        _ = action  # Unused
        window.show_sub_window(
            # The first argument is the class of the SettingsWindow
            SettingsWindow,
            # We must pass the settings instance to the SettingsWindow with the keyword argument "settings"
            settings=settings,
            # for SettingsWindow, modal=True is necessary
            modal=True,
            # Additionally, we can customize the appearance of the SettingsWindow, such as the title, the text of the
            # buttons, etc., with a SettingsWindowConfig object
            config=SettingsWindowConfig(
                title="Application Settings",
                content_title="Connection Options",
                confirm_button_text="Save Changes",
                cancel_button_text="Discard Changes",
                allow_restore_defaults=True,
                restore_defaults_button_text="Restore Defaults",
            ),
        )
        # Once the SettingsWindow is closed, the changes will be automatically saved to the settings instance
        # Here we can save the modified settings. For example save them to a file:

        # with open("settings.json", "w") as f:
        #     f.write(settings.serialize())

    file_menu = Menu(
        title="File",
        actions=[Action(text="Settings", on_triggered=on_action_show_settings)],
    )

    pyguiadapterlite.set_locale_code("en_US")  # set language

    adapter = GUIAdapter(dpi_aware=True)  # enable high DPI support
    adapter.add(
        my_app_function,
        # add menus to the window
        window_menus=[file_menu],
        # customize the appearance of the window
        window_config=FnExecuteWindowConfig(
            title="My App",  # set the title of the window
            print_function_result=False,  # don't print the result of the function to the console of the window
            show_function_result=False,  # don't show the result of the function in a message box
        ),
    )
    adapter.run()
    # app exited here
    # we can save the settings here. For example:

    # with open("settings.json", "w") as f:
    #     f.write(settings.serialize())
