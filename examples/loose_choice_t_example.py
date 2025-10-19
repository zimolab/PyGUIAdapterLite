from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import loose_choice_t, LooseChoiceValue


def loose_choice_example(arg1: loose_choice_t, arg2: loose_choice_t):
    uprint(f"arg1: {arg1}")
    uprint(f"arg2: {arg2}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        loose_choice_example,
        arg1=LooseChoiceValue(
            label="Your choice",
            choices=["a", "b", "c"],
            default_value="b",
            readonly=False,
            add_user_input=True,
            description="Choose one of the options",
        ),
        arg2=LooseChoiceValue(
            label="Another choice",
            choices=["a", "b", "c"],
            default_value="b",
            readonly=True,
            description="Choose one of the options",
        ),
    )
    adapter.run()
