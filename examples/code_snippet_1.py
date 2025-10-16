def sum_two_numbers(a: int, b: int) -> int:
    """
    计算两个整数之和。

    Args:
        a: 第一个整数。
        b: 第二个整数。

    Returns:
        两个整数之和。
    """
    return a + b


if __name__ == "__main__":
    from pyguiadapterlite import GUIAdapter

    adapter = GUIAdapter()
    adapter.add(sum_two_numbers)
    adapter.run()
