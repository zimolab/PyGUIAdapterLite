from pyguiadapterlite import GUIAdapter, uprint
from pyguiadapterlite.core.paramgroup import ParametersGroupBase
from pyguiadapterlite.types import IntValue, FloatValue


class ParameterGroup1(ParametersGroupBase):
    p1: int = IntValue(label="Parameter 1")
    p2: float = FloatValue(label="Parameter 2")


class ParameterGroup2(ParametersGroupBase):
    p1: int = IntValue(label="Parameter 1")
    p2: float = FloatValue(label="Parameter 2")


def foo(arg1: ParameterGroup1, arg2: ParameterGroup2):
    uprint(arg1, arg2)
    uprint(arg1.p1)
    uprint(arg1.p2)
    uprint(arg2.p1)
    uprint(arg2.p2)
    # how to raise a ParameterError on the parameter of a ParameterGroupedBase instance
    if arg1.p1 <= 0:
        arg1.raise_parameter_error("p1", "p1 should be positive")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add_parameters_grouped(foo)
    adapter.run()
