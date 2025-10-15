from typing import Literal

from pyguiadapterlite import uprint, FnExecuteWindow, Action, Menu, GUIAdapter
from pyguiadapterlite.types import choices_t, choice_t


def load_and_save_demo(
    arg1: int,
    arg2: float,
    arg3: bool,
    arg4: str,
    arg5: choices_t = (
        "apple",
        "banana",
        "orange",
        "pear",
        "grape",
        "pineapple",
        "watermelon",
        "kiwi",
    ),
    arg6: choice_t = ("java", "python", "javascript", "c++", "c#"),
    arg7: Literal["opt1", "opt2", "opt3"] = "opt2",
):
    """
    This demo shows how to save the parameters to a file and load them back later.
    """
    uprint(f"arg1: {arg1}, arg2: {arg2}, arg3: {arg3}, arg4: {arg4}")
    uprint(f"arg5: {arg5}")
    uprint(f"arg6: {arg6}")
    uprint(f"arg7: {arg7}")


if __name__ == "__main__":

    # prepare actions and window menu
    def save_params(wind: FnExecuteWindow, action: Action):
        print("Save current parameters of the window to a file")
        wind.save_parameter_values()

    def load_params(wind: FnExecuteWindow, action: Action):
        print("Load parameters from a file and apply to the window")
        wind.load_parameter_values()

    action_save = Action("Save Parameters", save_params, shortcut="Control-s")
    action_load = Action("Load Parameters", load_params, shortcut="Control-l")

    menu_file = Menu(title="File", actions=[action_save, action_load])

    adapter = GUIAdapter()
    # add the function and set the window menus of it
    adapter.add(load_and_save_demo, window_menus=[menu_file])
    # run the adapter
    adapter.run()
