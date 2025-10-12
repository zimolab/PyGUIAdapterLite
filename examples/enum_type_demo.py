from enum import Enum

from pyguiadapterlite import GUIAdapter, uprint


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Fruit(Enum):
    APPLE, BANANA, ORANGE, MANGO = range(4)


def enum_type_demo(arg1: Color, fruit: Fruit = Fruit.ORANGE):
    uprint(f"arg1: {arg1}")
    uprint(f"fruit: {fruit}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(enum_type_demo)
    adapter.run()
