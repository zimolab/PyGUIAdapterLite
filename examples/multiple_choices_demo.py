from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import MultiChoiceValue
from pyguiadapterlite.types.extendtypes import choices_t


def multiple_choice_demo(
    arg1: choices_t,
    arg2: choices_t,
    arg3: choices_t = (
        "apple",
        "banana",
        "orange",
        "pear",
        "grape",
        "pineapple",
        "watermelon",
        "kiwi",
    ),
):
    """
    Demo of multiple choice parameters.

    :param arg1: this parameter is configured in the docstring
    :param arg2: this parameter is configured with the choices parameter of GUIAdapter.add() method
    :param arg3: this choices of this parameter is from its default value
    :return:

    @params
    [arg1]
    __type__ = "choices_t"
    choices = ["Jave", "Python", "JavaScript", "C++", "JavaScript", "Rust", "Swift"]
    default_value = ["Python", "JavaScript", "Swift"]
    columns = 3
    @end

    """
    uprint("arg1 = ", arg1)
    uprint("arg2 = ", arg2)
    uprint("arg3 = ", arg3)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        multiple_choice_demo,
        widget_configs={
            "arg2": MultiChoiceValue(
                choices={
                    "Apple": 1,
                    "Banana": 2,
                    "Orange": 3,
                    "Pear": 4,
                    "Grape": 5,
                    "Pineapple": 6,
                    "Watermelon": 7,
                },
                default_value=(1, 3, 5),
                columns=4,
                hide_label=False,
                content_title="Choose Fruits",
            )
        },
    )
    adapter.run()
