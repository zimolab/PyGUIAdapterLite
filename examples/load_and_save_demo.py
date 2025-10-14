from pyguiadapterlite import uprint, FnExecuteWindow, Action, Menu, GUIAdapter


def load_and_save_demo(arg1: int, arg2: float, arg3: bool, arg4: str):
    """
    This demo shows how to save the parameters to a file and load them back later.
    """
    uprint(f"arg1: {arg1}, arg2: {arg2}, arg3: {arg3}, arg4: {arg4}")


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
