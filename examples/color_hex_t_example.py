from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import color_hex_t, color_t, HexColorValue


def foo(color1: color_hex_t, color2: color_t):
    uprint(f"color1: {color1}")
    uprint(f"color2: {color2}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        color1=HexColorValue(
            label="Color 1",
            default_value="#FF0000",
            color_picker_title="Choose a color",
            show_color_code=True,
        ),
        color2=HexColorValue(
            label="Color 2",
            default_value="#00FF00",
            color_picker_title="Pick a color",
            show_color_code=False,
        ),
    )
    adapter.run()
