import os.path

from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import file_t, FileValue


def foo(x: file_t):
    uprint(f"x: {x}, {os.path.isfile(x)}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        x=FileValue(
            label="File",
            default_value="abc.txt",
            start_dir=os.curdir,
            save_file=False,
            filters=[
                ("Python files", "*.py"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
            select_button_text="Select",
            normalize_path=True,
            absolutize_path=True,
            readonly=True,
            allow_backspace=True,
            description="Select a file to open",
        ),
    )
    adapter.run()
