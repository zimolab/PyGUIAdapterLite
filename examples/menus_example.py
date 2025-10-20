from pyguiadapterlite import (
    uprint,
    GUIAdapter,
    Menu,
    FnExecuteWindow,
    Action,
    Separator,
)
from pyguiadapterlite.utils import show_information, show_question


def _on_action_open(window: FnExecuteWindow, action: Action):
    print("Action Open triggered")
    show_information("Action Open triggered", parent=window.parent)


def _on_action_save(window: FnExecuteWindow, action: Action):
    print("Action Save triggered")
    show_information("Action Save triggered", parent=window.parent)


def _on_action_close(window: FnExecuteWindow, action: Action):
    print("Action Close triggered")
    ret = show_question("Are you sure to close the window?", parent=window.parent)
    if ret == "yes":
        window.close()


def _on_action_about(window: FnExecuteWindow, action: Action):
    print("Action About triggered")
    show_information("Action About triggered", parent=window.parent)


def _on_action_help(window: FnExecuteWindow, action: Action):
    print("Action Help triggered")
    show_information("Action Help triggered", parent=window.parent)


def foo(arg1: str, arg2: int):
    uprint(f"arg1 is {arg1} and arg2 is {arg2}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        window_menus=[
            Menu(
                title="File",
                actions=[
                    Action(
                        text="Open", on_triggered=_on_action_open, shortcut="Control-o"
                    ),
                    Action(
                        text="Save", on_triggered=_on_action_save, shortcut="Control-s"
                    ),
                    Separator(),
                    Action(
                        text="Close",
                        on_triggered=_on_action_close,
                        shortcut="Control-w",
                    ),
                ],
            ),
            Menu(
                title="Help",
                actions=[
                    Action(text="About", on_triggered=_on_action_about),
                    Action(text="Help", on_triggered=_on_action_help),
                ],
            ),
        ],
    )
    adapter.run()
