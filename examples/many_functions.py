from pyguiadapterlite import GUIAdapter
from pyguiadapterlite.types import dir_t, bool_t, DirectoryValue, BoolValue2


def convert_to_pngs(input_dir: dir_t, output_dir: dir_t, recursive: bool_t = False):
    """Converts all image files in the input directory to PNG format and saves them in the output directory."""
    pass


def convert_to_pdfs(input_dir: dir_t, output_dir: dir_t, recursive: bool_t = False):
    """Converts all image files in the input directory to PDF format and saves them in the output directory."""
    pass


def convert_to_jpgs(input_dir: dir_t, output_dir: dir_t, recursive: bool_t = False):
    """Converts all image files in the input directory to JPG format and saves them in the output directory."""
    pass


PARAM_CONFS = {
    "input_dir": DirectoryValue(
        label="Input Directory",
        default_value="",
        start_dir="./",
        dialog_title="Select Input Directory",
        select_button_text="Browse",
        normalize_path=True,
        absolutize_path=True,
    ),
    "output_dir": DirectoryValue(
        label="Output Directory",
        default_value="",
        start_dir="./",
        dialog_title="Select Output Directory",
        select_button_text="Browse",
        normalize_path=True,
        absolutize_path=True,
    ),
    "recursive": BoolValue2(
        label="Find files recursively",
        default_value=False,
    ),
}

if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        convert_to_pngs, display_name="PNG Converter", widget_configs=PARAM_CONFS
    )
    adapter.add(
        convert_to_pdfs, display_name="PDF Converter", widget_configs=PARAM_CONFS
    )
    adapter.add(
        convert_to_jpgs, display_name="JPG Converter", widget_configs=PARAM_CONFS
    )
    adapter.run()
