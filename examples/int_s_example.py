from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import int_s, ScaleIntValue2


def foo(x: int_s, y: int_s):
    uprint(f"x: {x}")
    uprint(f"y: {y}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        widget_configs={
            "x": ScaleIntValue2(
                label="Parameter X",
                default_value=25,
                min_value=0,
                max_value=50,
                show_value=True,
                cursor="hand2",
                tick_interval=5,
                step=5,
                description="This is a description",
            ),
            "y": ScaleIntValue2(
                label="Parameter Y",
                default_value=75,
                min_value=50,
                max_value=100,
                show_value=False,
                tick_interval=10,
                cursor="arrow",
                step=10,
                description="This is a description",
            ),
        },
    )
    adapter.run()
