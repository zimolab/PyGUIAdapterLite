from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import string_list, str_list, StringListValue


def foo(arg1: string_list, arg2: str_list):
    uprint("arg1:", arg1)
    uprint("arg2:", arg2)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        arg1=StringListValue(
            label="String List 1",
            default_value=[
                "Hello",
                "World",
                "Honestly I don't know what to write here",
            ],
            add_button=True,
            add_button_text="Add",
            add_method="append",
            strip=False,
            accept_empty=True,
            accept_duplicates=True,
        ),
        arg2=StringListValue(
            label="String List 2",
            default_value=["foo", "bar", "baz"],
            add_button=True,
            add_button_text="New Item",
            add_method="append",
            strip=True,
            accept_empty=False,
            accept_duplicates=False,
        ),
    )
    adapter.run()
