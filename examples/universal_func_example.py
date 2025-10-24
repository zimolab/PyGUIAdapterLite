from pyguiadapterlite import GUIAdapter, uprint
from pyguiadapterlite.types import TextValue, IntValue
from pyguiadapterlite.types.nonvalues import MessageLabelConfig
from pyguiadapterlite.types.nonvalues.button import ButtonConfig, ButtonWidget


def universal_function(**kwargs):
    for k, v in kwargs.items():
        uprint(f"{k}={v}")


def normal_function(x: int, y: int, z: int, e: int = 40):
    uprint(f"x={x}, y={y}, z={z}, e={e}")


def on_button_click(button: ButtonWidget):
    print("Button clicked")
    print(button.current_window.get_parameter_values())


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add_universal(
        fn=universal_function,
        parameter_configs={
            "arg1": TextValue(label="Arg1", default_value="hello"),
            "arg2": IntValue(label="Arg2", default_value=10),
            "message": MessageLabelConfig(text="This is a message"),
            "button": ButtonConfig(text="Click me", on_click=on_button_click),
            "arg3": {
                "__type__": "float_ss",
                "default_value": 3.14,
            },
        },
        x=IntValue(label="X", default_value=10),
        y=IntValue(label="Y", default_value=20),
        z=IntValue(label="Z", default_value=30),
        e={
            "__type__": "float_ss",
            "default_value": 40,
        },
    )
    adapter.add(normal_function)
    adapter.run()
