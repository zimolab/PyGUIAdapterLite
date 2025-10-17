from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import path_list_t


def path_list_example(path_list_arg: path_list_t):
    for path in path_list_arg:
        uprint(path)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(path_list_example)
    adapter.run()
