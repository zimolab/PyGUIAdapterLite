from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import bool_t, BoolValue2


def foo(arg1: bool_t, arg2: bool_t):
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        widget_configs={
            "arg1": BoolValue2(
                default_value=True,
                hint_text="Whether to enable arg1 or not",
                description="This is a bool value with check box",
            ),
            "arg2": BoolValue2(
                default_value=False,
                hint_text="Whether to enable arg2 or not",
                hide_label=False,
                description="This is a bool value with check box",
            ),
        },
    )
    adapter.run()
