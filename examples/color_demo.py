from pyguiadapterlite import GUIAdapter, uprint
from pyguiadapterlite.types.extendtypes import color_hex_t


def color_demo(color1: color_hex_t, color2: color_hex_t = "#FFEE00"):
    uprint(f"Color 1: {color1}")
    uprint(f"Color 2: {color2}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(color_demo)
    adapter.run()
