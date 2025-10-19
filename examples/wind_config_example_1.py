from pyguiadapterlite import (
    GUIAdapter,
    uprint,
    FnSelectWindowConfig,
    FnExecuteWindowConfig,
)
from pyguiadapterlite.types import dir_t


def convert_pngs(input_dir: dir_t, output_dir: dir_t):
    """Convert PNGs to JPGs."""
    uprint(f"Converting PNGs from {input_dir} to {output_dir}")


def converts_gifs(input_dir: dir_t, output_dir: dir_t):
    """Convert GIFs to PNGs."""
    uprint(f"Converting GIFs from {input_dir} to {output_dir}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        convert_pngs,
        display_name="PNG Converter",
        window_config=FnExecuteWindowConfig(
            title="PNG Converter",
            icon="pic_32.ico",
            execute_button_text="Convert",
            clear_button_text="Clear Output",
            clear_checkbox_visible=False,
            default_parameter_group_name="Input/Output",
            output_tab_title="Output",
            output_background="#300A24",
            document_tab_title="Description",
            show_function_result=False,
            print_function_result=False,
        ),
    )
    adapter.add(converts_gifs, display_name="GIF Converter", icon="gif_64.ico")
    adapter.run(
        select_window_config=FnSelectWindowConfig(
            title="Image ToolBox",
            icon="toolkit_64.ico",
            select_button_text="Go",
            function_list_title="Image Tools",
            document_view_title="Description",
            no_document_text="No description available",
            no_selection_status_text="Please select an image tool",
            current_view_status_text="Current Function: ",
        )
    )
