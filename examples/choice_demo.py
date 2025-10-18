from pyguiadapterlite import GUIAdapter, uprint
from pyguiadapterlite.types import LooseChoiceValue
from pyguiadapterlite.types.extendtypes import choice_t


def loose_choice_demo(
    arg1: choice_t, arg2: choice_t, arg3: choice_t = ("choice1", "choice2", "choice3")
):
    """
    Demo for loose choice type(choice_t)

    :param arg1: this parameter is configured in docstring
    :param arg2: this parameter is configured with widget_configs parameter of GUIAdapter.add() method
    :param arg3: the available choices of this parameter is from its default value.
    :return:

    @params
    [arg1]
    __type__ = "choice_t"
    choices = ["apple", "banana", "orange", "pear", "grape", "pineapple", "watermelon"]
    default_value = "pineapple"
    readonly = false
    add_user_input = true
    @end

    """
    uprint(f"arg1: {arg1}, arg2: {arg2}, arg3: {arg3}")


if __name__ == "__main__":
    adapter = GUIAdapter()

    adapter.add(
        loose_choice_demo,
        widget_configs={
            "arg2": LooseChoiceValue(
                default_value="C++",
                choices=[
                    "Python",
                    "Java",
                    "C++",
                    "Ruby",
                    "Swift",
                    "Kotlin",
                    "Go",
                    "Scala",
                ],
                readonly=True,
                add_user_input=False,
            )
        },
    )

    adapter.run()
