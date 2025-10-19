from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import dir_list, DirectoryListValue


def foo(dir_paths: dir_list):
    uprint("dir_paths:", dir_paths)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        dir_paths=DirectoryListValue(
            label="Include Paths",
            default_value=["/usr/include", "/usr/local/include"],
            start_dir="/",
            add_button_text="Add Include Path",
            add_path_dialog_label_text="Select Include Path",
            add_dir_button_text="Add Include Directory",
            dir_dialog_title="Select Include Directory",
            strip=True,
            accept_empty=False,
            accept_duplicates=False,
            normalize_path=False,
            absolutize_path=True,
        ),
    )
    adapter.run()
