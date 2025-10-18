from typing import Literal
from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import SingleChoiceValue


def foo(
    arg1: Literal["choice1", "choice2", "choice3", "choice4"],
    arg2: Literal[32, 64, 128, 256, 512, 1024, 2048],
):
    uprint(f"arg1: {arg1}, type: {type(arg1)}")
    uprint(f"arg2: {arg2}, type: {type(arg2)}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo, widget_configs={"arg2": SingleChoiceValue(columns=4)})
    adapter.run()
