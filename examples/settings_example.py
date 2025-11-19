from pyguiadapterlite import FnExecuteWindow, Action, GUIAdapter, Menu
from pyguiadapterlite.components.settingsbase import JsonSettingsBase
from pyguiadapterlite.types import (
    FloatValue,
    FileValue,
    DirectoryValue,
    LooseChoiceValue,
    StringValue,
)
from pyguiadapterlite.windows.settingswindow import SettingsWindow, SettingsWindowConfig


class AppSettings(JsonSettingsBase):
    volume = FloatValue(label="Volume", default_value=0.5)
    path = FileValue(label="Data File")
    directory = DirectoryValue(label="Save Directory")
    language = LooseChoiceValue(
        label="Language", choices=["en", "fr", "es"], readonly=True
    )
    app_key = StringValue(label="App Key", default_value="1234567890")


settings = AppSettings()


def settings_example(x: int, y: float, z: str, a: bool):
    pass


def on_action_settings(window: FnExecuteWindow, action: Action):

    # we can use a factory function to filter out the fields that
    # we don't want to show in the settings window so that the user
    # can't see or modify them.
    # In this example, we remove the "app_key" field from the settings window.
    def setting_fields_factory(settings_: AppSettings):
        fields = settings_.__class__.fields()
        fields.pop("app_key")
        return fields

    # This function will be called when user click the "Save" button
    # in the settings window and all the fields are valid.
    # the "settings" parameter is the updated is the same instance as you passed
    # to the "show_sub_window" method with updated values.
    def after_settings_saved(settings_: AppSettings):
        # you can save the settings to a file or database he here
        # settings_.save(file_path="settings.json")
        print(f"Settings edited: {settings_}")

    # If we want to show all the fields in the settings window,
    # don't specify the "setting_fields" parameter or pass None to it.
    window.show_sub_window(
        SettingsWindow,
        config=SettingsWindowConfig(title="App Settings"),
        settings=settings,
        setting_fields=setting_fields_factory,
        after_save_callback=after_settings_saved,
        modal=True,
    )


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        settings_example,
        window_menus=[
            Menu(
                title="Settings",
                actions=[Action(text="Settings", on_triggered=on_action_settings)],
            )
        ],
    )
    adapter.run()
