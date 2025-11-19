from pyguiadapterlite import GUIAdapter, Action, FnExecuteWindow, Menu
from pyguiadapterlite.types import IntValue
from pyguiadapterlite.windows.objectwindow import (
    ObjectWindow,
    ObjectWindowConfig,
)


def foo(x: int):
    pass


if __name__ == "__main__":

    my_obj_schema = {
        "x": IntValue(label="X", default_value=10, description="X value"),
        "y": IntValue(label="Y", default_value=20, description="Y value"),
        "z": IntValue(label="Z", default_value=30, description="Z value"),
    }
    my_obj = {"x": 0, "y": 0}

    def on_action_edit_obj(window: FnExecuteWindow, action: Action):
        print("before edited: ", my_obj)
        window.show_sub_window(
            ObjectWindow,
            ObjectWindowConfig(
                object_schema=my_obj_schema,
                initial_object=my_obj,
            ),
            modal=True,
        )
        print("after edited: ", my_obj)

    menus = [Menu("File", actions=[Action("Edit Object", on_action_edit_obj)])]

    adapter = GUIAdapter()
    adapter.add(foo, window_menus=menus)
    adapter.run()
