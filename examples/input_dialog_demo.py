from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.core.context import (
    get_string_input,
    get_int_input,
    get_float_input,
)


def input_dialog_demo(
    get_string_prompt: str = "Enter a string:",
    get_int_prompt: str = "Enter an integer:",
    get_float_prompt: str = "Enter a float:",
):
    ret = get_string_input(prompt=get_string_prompt)
    uprint(f"String input: {ret}")
    ret = get_int_input(prompt=get_int_prompt)
    uprint(f"Integer input: {ret}")
    ret = get_float_input(prompt=get_float_prompt)
    uprint(f"Float input: {ret}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(input_dialog_demo)
    adapter.run()
