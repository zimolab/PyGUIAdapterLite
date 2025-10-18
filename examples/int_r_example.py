from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import int_r, RangedIntValue


def foo(x: int_r, y: int_r):
    uprint(f"x: {x}")
    uprint(f"y: {y}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        widget_configs={
            "x": RangedIntValue(
                label="Parameter X",
                min_value=0,
                max_value=100,
                step=1,
                wrap=True,
                default_value=50,
                description="This is parameter X",
            ),
            "y": RangedIntValue(
                label="Parameter Y",
                min_value=-100,
                max_value=100,
                step=1,
                wrap=True,
                default_value=-50,
                description="This is parameter Y",
            ),
        },
    )
    adapter.run()
