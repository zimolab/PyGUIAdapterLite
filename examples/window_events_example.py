from pyguiadapterlite import FnExecuteWindow, GUIAdapter, uprint
from pyguiadapterlite.utils import show_information, show_question


def foo(a: int, b: str):
    uprint(f"a={a}")
    uprint(f"b={b}")


def after_window_created(window: FnExecuteWindow):
    print("Window created")
    window.parent.after(
        500, lambda: show_information("Hello, world!", parent=window.parent)
    )


def before_window_closed(window: FnExecuteWindow) -> bool:
    print("Window closing")
    if (
        show_question("Are you sure to close the window?", parent=window.parent)
        == "yes"
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        after_window_create_callback=after_window_created,
        before_window_close_callback=before_window_closed,
    )
    adapter.run()
