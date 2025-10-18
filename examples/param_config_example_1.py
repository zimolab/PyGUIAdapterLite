from pyguiadapterlite import uprint, GUIAdapter


def my_function_1(
    param1: int = 100,
    param2: str = "Hello World",
    param3: float = 3.14,
    param4: bool = True,
):
    """
    This is the function description.
    :param param1: description of the param1
    :param param2: description of the param2
    :param param3: description of the param3
    :param param4: description of the param4
    :return:
    """
    uprint(f"param1: {param1}")
    uprint(f"param2: {param2}")
    uprint(f"param3: {param3}")
    uprint(f"param4: {param4}")


def my_function_2(
    param1: int = 100,
    param2: str = "Hello World",
    param3: float = 3.14,
    param4: bool = True,
):
    """
    This is the function description.
    Args:
        param1: description of the param1
        param2: description of the param2
        param3: description of the param3
        param4: description of the param4

    Returns:

    """
    uprint(f"param1: {param1}")
    uprint(f"param2: {param2}")
    uprint(f"param3: {param3}")
    uprint(f"param4: {param4}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(my_function_1)
    adapter.add(my_function_2)
    adapter.run()
