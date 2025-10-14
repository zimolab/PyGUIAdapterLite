from typing import Literal

from pyguiadapterlite import GUIAdapter, FnExecuteWindowConfig
from pyguiadapterlite.core.context import show_toast
from pyguiadapterlite.types import text_t, color_hex_t


def toast_example(
    message: text_t = "Hello world!",
    duration: int = 3000,
    position: Literal["top", "bottom", "center"] = "top",
    foreground_color: color_hex_t = "#FFFFFF",
    background_color: color_hex_t = "#323232",
):
    if not message:
        show_toast("Please provide a message to display.")
        return
    show_toast(
        message,
        duration=duration,
        position=position,
        foreground=foreground_color,
        background=background_color,
    )


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        toast_example,
        window_config=FnExecuteWindowConfig(
            title="Toast Example", show_function_result=False
        ),
    )
    adapter.run()
