from pyguiadapterlite import GUIAdapter, uprint


def foo(message: str = "Hello World!"):
    uprint(message)
    uprint(f"\x1b[1m{message}\x1b[0m")
    uprint(f"\x1b[3m{message}\x1b[0m")
    uprint(f"\x1b[4m{message}\x1b[0m")
    uprint(f"\x1b[7m{message}\x1b[0m")
    uprint(f"\x1b[6m{message}\x1b[0m")
    uprint(f"\x1b[5m{message}\x1b[0m")
    uprint(f"\x1b[31m{message}\x1b[0m")
    uprint(f"\x1b[32m{message}\x1b[0m")
    uprint(f"\x1b[33m{message}\x1b[0m")
    uprint(f"\x1b[34m{message}\x1b[0m")
    uprint(f"\x1b[35m{message}\x1b[0m")
    uprint(f"\x1b[36m{message}\x1b[0m")
    uprint("")

    # 组合样式
    uprint(f"\x1b[1;31m{message}\x1b[0m")
    uprint(f"\x1b[1;32;44m{message}\x1b[0m")
    uprint(f"\x1b[1;4;33m{message}\x1b[0m")
    uprint("")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run()
