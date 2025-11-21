from pyguiadapterlite import GUIAdapter, set_logging_enabled

# Disable logging messages from pyguiadapterlite
set_logging_enabled(False)


def foo():
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run()
