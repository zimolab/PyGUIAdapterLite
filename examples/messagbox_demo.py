from pyguiadapterlite import GUIAdapter
from pyguiadapterlite.core.context import (
    show_info_messagebox,
    show_warning_messagebox,
    show_critical_messagebox,
    show_question_messagebox,
    uprint,
    show_ok_cancel_messagebox,
    show_retry_cancel_messagebox,
    show_yes_no_cancel_messagebox,
    show_yes_no_messagebox,
)
from pyguiadapterlite.types import text_t


def messagebox_demo(
    info_msg: text_t = "this is an info message",
    warning_msg: text_t = "this is a warning message",
    error_msg: text_t = "this is an error message",
):
    show_info_messagebox(title="Info Message", message=f"You input: {info_msg}")
    show_warning_messagebox(title="Warning Message", message=warning_msg)
    show_critical_messagebox(title="Critical Message", message=error_msg)
    ret = show_question_messagebox(
        "Yes or No?", "This is a question message with Yes or No buttons."
    )
    uprint(f"You choose: {ret}")
    ret = show_ok_cancel_messagebox(
        "OK or Cancel?",
        "This is a messagebox with OK or Cancel decision. Ok will return True, Cancel will return False.",
    )
    uprint(f"You choose: {ret}")
    ret = show_retry_cancel_messagebox(
        "Retry or Cancel?",
        "This is a messagebox with Retry or Cancel decision. Retry will return True, Cancel will return False.",
    )
    uprint(f"You choose: {ret}")
    ret = show_yes_no_cancel_messagebox(
        "Yes, No or Cancel?",
        "This is a messagebox with Yes, No or Cancel decision. Yes will return True, No will return False, Cancel will return None.",
    )
    uprint(f"You choose: {ret}")
    ret = show_yes_no_messagebox(
        "Yes or No?",
        "This is a messagebox with Yes or No decision. Yes will return True, No will return False.",
    )
    uprint(f"You choose: {ret}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(messagebox_demo)
    adapter.run()
