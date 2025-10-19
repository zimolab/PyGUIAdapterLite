from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import float_s, ScaleFloatValue


def foo(x: float_s, y: float_s):
    uprint("x: ", x)
    uprint("y: ", y)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        x=ScaleFloatValue(
            label="Parameter X",
            default_value=50.12,
            min_value=0.0,
            max_value=100.0,
            digits=2,
            show_value=True,
            description="This is the X parameter",
        ),
        y=ScaleFloatValue(
            label="Parameter Y",
            default_value=175.34,
            min_value=100.0,
            max_value=200.0,
            digits=5,
            show_value=False,
            description="This is the Y parameter",
        ),
    )
    adapter.run()
