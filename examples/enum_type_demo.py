from enum import Enum

from pyguiadapterlite import GUIAdapter, uprint
from pyguiadapterlite.types.choices.enumchoice import EnumValue


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Fruit(Enum):
    APPLE, BANANA, ORANGE, MANGO = range(4)


class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


def enum_type_demo(color: Color, fruit: Fruit, day: Weekday = Weekday.SUNDAY):
    """
    Demo for enum types.

    :param color: parameter with enum type Color
    :param fruit: parameter with enum type Fruit, configured with widget_configs parameter of GUIAdapter.add()
    :param day: parameter with enum type Weekday, with default value SUNDAY
    :return:
    """
    uprint(f"arg1: {color}")
    uprint(f"fruit: {fruit}")
    uprint(f"day: {day}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        enum_type_demo,
        widget_configs={
            "fruit": EnumValue(
                default_value=Fruit.BANANA,
                description="parameter with enum type Fruit, configured with widget_configs parameter of GUIAdapter.add()",
                columns=2,
                hide_label=False,
                content_title="Your favorite fruit",
                enum_class=Fruit,
            )
        },
    )
    adapter.run()
