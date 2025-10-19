import os

from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import path_list_t, PathListValue


def foo(paths_1: path_list_t):
    uprint("paths_1:", paths_1)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        paths_1=PathListValue(
            label="Files and Directories",
            default_value=["/usr/include", "/usr/local/include"],
            add_button_text="Include",
            start_dir=os.path.expanduser("~"),
            filters=[("Header files", "*.h"), ("All files", "*")],
            file_dialog_title="Select File",
            dir_dialog_title="Select Directory",
            add_file_button_text="Add File",
            add_dir_button_text="Add Directory",
            strip=True,
            accept_empty=False,
            accept_duplicates=False,
            normalize_path=True,
            absolutize_path=True,
        ),
    )
    adapter.run()
