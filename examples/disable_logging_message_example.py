import os

os.environ["PYGUIADAPTERLITE_LOGGING_MESSAGE"] = "0"

from pyguiadapterlite import GUIAdapter


def foo():
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run()
