from pyguiadapterlite import GUIAdapter, uprint
from pyguiadapterlite.types import file_t


def foo(str_arg: str, file_arg: file_t):
    """
    这个示例演示str、file_t类型参数控件的差异。

    Args:
        str_arg: 字符串参数。
        file_arg: 文件路径参数。

    """
    uprint(f"str_arg: {str_arg}")
    uprint(f"file_arg: {file_arg}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run()
