from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import int_ss, ScaleIntValue


def foo(x: int_ss, y: int_ss):
    uprint(f"x: {x}")
    uprint(f"y: {y}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        widget_configs={
            "x": ScaleIntValue(
                label="Parameter X",
                default_value=10,
                min_value=0,
                max_value=100,
                show_value=True,
                cursor="hand2",
                description="This is parameter x",
            ),
            "y": ScaleIntValue(
                label="Parameter Y",
                default_value=20,
                min_value=0,
                max_value=100,
                show_value=False,
                cursor="arrow",
                description="This is parameter y",
            ),
        },
    )
    adapter.run()
