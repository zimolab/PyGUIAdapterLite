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
    adapter.add(
        foo,
        widget_configs={
            "arg1": SingleChoiceValue(
                default_value="choice1",
                choices=["choice1", "choice2", "choice3", "choice4"],
                content_title="Choose an option",
                hide_label=False,
                description="Choose an option for the first argument",
            ),
            "arg2": SingleChoiceValue(
                default_value=1024,
                content_title="Choose a size",
                columns=4,
                description="Choose a size for the new file",
            ),
        },
    )
    adapter.run()
