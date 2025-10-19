from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import text_t, TextValue


def foo(x: text_t):
    uprint(x)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        x=TextValue(
            label="Input Text",
            default_value="Hello, world!",
            wrap="word",
            font=("Arial", 12),
        ),
    )
    adapter.run()
