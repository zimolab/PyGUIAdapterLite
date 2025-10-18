import sys

from pyguiadapterlite import GUIAdapter


def test_fix(a: int, b: int):
    print("Test Fix 1")
    sys.exit(-1)


if __name__ == "__main__":
    adapter = GUIAdapter()
    # adapter.add(test_fix, capture_system_exit_exception=True)
    adapter.add(test_fix, capture_system_exit_exception=False)
    adapter.run()
