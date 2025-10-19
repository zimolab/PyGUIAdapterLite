from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import file_list, FileListValue


def foo(files_arg: file_list):
    uprint("files:", files_arg)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        files_arg=FileListValue(
            label="Library Files",
            default_value=["a.lib", "b.lib", "c.lib"],
            filters=[("Library Files", "*.lib"), ("All Files", "*.*")],
            start_dir="./",
            strip=True,
            absolutize_path=True,
            normalize_path=True,
            accept_duplicates=False,
            accept_empty=False,
            add_button_text="Add Library",
            add_file_button_text="Select Library File",
            add_method="prepend",
            file_dialog_title="Select Library File",
        ),
    )
    adapter.run()
