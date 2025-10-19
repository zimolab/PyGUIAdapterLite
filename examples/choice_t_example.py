from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import choice_t, SingleChoiceValue


def choice_t_example(arg1: choice_t, arg2: choice_t):
    uprint(f"arg1: {arg1}, type: {type(arg1)}")
    uprint(f"arg2: {arg2}, type: {type(arg2)}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        choice_t_example,
        arg1=SingleChoiceValue(
            label="Favorite language",
            choices={
                "Python": 1,
                "C/C++": 2,
                "Java": 3,
                "JavaScript": 4,
                "C#": 5,
                "Swift": 6,
            },
            default_value=1,
            columns=2,
            hide_label=True,
        ),
        arg2=SingleChoiceValue(
            label="Your choice",
            choices=["Option 1", "Option 2", "Option 3", "Option 4"],
            default_value="Option 2",
            columns=1,
        ),
    )
    adapter.run()
