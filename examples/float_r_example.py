from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import float_r, RangedFloatValue


def foo(x: float_r, y: float_r):
    uprint(f"x: {x}")
    uprint(f"y: {y}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        x=RangedFloatValue(
            label="Parameter X",
            default_value=1.0,
            min_value=0.5,
            max_value=10.0,
            step=0.1,
            decimals=5,
            auto_correct=False,
            description="This is a description of parameter X",
        ),
        y=RangedFloatValue(
            label="Parameter Y",
            default_value=5.0,
            min_value=-10.0,
            max_value=10.0,
            step=0.005,
            decimals=3,
            auto_correct=True,
            correct_to="nearest",
            description="This is a description of parameter Y",
        ),
    )
    adapter.run()
