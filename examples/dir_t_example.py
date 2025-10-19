import os

from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import directory_t, dir_t, DirectoryValue


def foo(x: directory_t, y: dir_t):
    uprint(f"x: {x}, exists: {os.path.exists(x)}")
    uprint(f"y: {y}, exists: {os.path.exists(y)}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        x=DirectoryValue(
            label="Directory 1",
            default_value=os.curdir,
            start_dir=os.getcwd(),
            readonly=False,
            normalize_path=True,
            absolutize_path=True,
            description="Directory 1 description",
        ),
        y=DirectoryValue(
            label="Directory 2",
            default_value=os.curdir,
            start_dir=os.getcwd(),
            readonly=True,
            allow_backspace=True,
            normalize_path=True,
            absolutize_path=True,
            description="Directory 2 description",
        ),
    )
    adapter.run()
