import os

from pyguiadapterlite import (
    uprint,
    GUIAdapter,
    get_path_input,
    get_file_path_input,
    get_dir_path_input,
)
from pyguiadapterlite import (
    get_string_input,
    get_int_input,
    get_float_input,
    get_string_input2,
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
    # input dialog implemented on custom dialog
    ret = get_string_input2(label_text="Enter the password:", echo_char="*")
    uprint(f"password: {ret}")
    ret = get_path_input(
        label_text="Select a file or directory:",
        file_types=[("All files", "*.*"), ("Python files", "*.py")],
        start_dir=os.getcwd(),
    )
    uprint(f"Selected: {ret}")
    ret = get_file_path_input(
        title="Select a file",
        start_dir=os.getcwd(),
        file_dialog_action="open",
        file_dialog_title="Open file",
        file_types=[("All files", "*.*"), ("Python files", "*.py")],
    )
    uprint(f"Selected file: {ret}")
    ret = get_dir_path_input(title="Select a directory", start_dir=os.getcwd())
    uprint(f"Selected directory: {ret}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(input_dialog_demo)
    adapter.run()
