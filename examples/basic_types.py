from pyguiadapterlite import GUIAdapter
from pyguiadapterlite.types import BoolValue


def basic_types(
    arg1: int,
    arg2: float,
    arg3: str = "default value",
    arg4: bool = BoolValue(
        default_value=True, true_text="Yes", false_text="No", orientation="vertical"
    ),
):
    """
    :param arg1: description of arg1
    :param arg2: description of arg2
    :param arg3: description of arg3
    :param arg4: description of arg4
    :return:
    """


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(basic_types)
    adapter.run()
