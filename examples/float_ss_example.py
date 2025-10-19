from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import float_ss, ScaleFloatValue2


def foo(x: float_ss, y: float_ss):
    uprint("x: ", x)
    uprint("y: ", y)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        x=ScaleFloatValue2(
            label="Parameter X",
            default_value=50.5,
            min_value=0.0,
            max_value=100.0,
            show_value=True,
            digits=6,
            step=0.5,
            tick_interval=10,
            description="This is the X parameter",
        ),
        y=ScaleFloatValue2(
            label="Parameter Y",
            default_value=175.5,
            min_value=100.0,
            max_value=200.0,
            step=10.5,
            digits=5,
            show_value=False,
            description="This is the Y parameter",
        ),
    )
    adapter.run()
