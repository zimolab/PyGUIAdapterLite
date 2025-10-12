from typing import Literal

from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import SingleChoiceValue


def single_choice_demo(
    arg1: Literal["foo", "bar", "baz"],
    arg2: Literal["spam", "eggs", "ham"] = "eggs",
    arg3: str = "apple",
    arg4: int = 1,
):
    """
    A demo to show how the Literal type parameters.
    :param arg1: arg1 can only be "foo", "bar", or "baz"
    :param arg2: arg2 can only be "spam", "eggs", or "ham" (default is "eggs")
    :param arg3: arg3 is configured in the docstring
    :param arg4: arg4 is configured with the widget_configs parameter of GUIAdapter.add() method
    :return:

    @params
    [arg3]
    __type__ = "Literal"
    choices = ["apple", "banana", "orange", "pear", "grape", "pineapple", "watermelon"]
    default_value = "pineapple"
    columns = 2
    @end

    """
    uprint("arg1 = ", arg1)
    uprint("arg2 = ", arg2)
    uprint("arg3 = ", arg3)
    uprint("arg4 = ", arg4)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        single_choice_demo,
        widget_configs={
            "arg4": SingleChoiceValue(
                choices={
                    "Apple": 1,
                    "Banana": 2,
                    "Orange": 3,
                    "Pear": 4,
                    "Grape": 5,
                    "Pineapple": 6,
                    "Watermelon": 7,
                },
                default_value=6,
                columns=4,
                hide_label=False,
                content_title="Choose a fruit",
            )
        },
    )
    adapter.run()
