from pyguiadapterlite import GUIAdapter


def foo():
    pass


if __name__ == "__main__":
    adapter = GUIAdapter(dpi_aware=True)
    adapter.add(foo)
    adapter.run()
