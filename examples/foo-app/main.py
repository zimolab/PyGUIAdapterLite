from foo_app.app import my_app
from pyguiadapterlite import GUIAdapter

if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(my_app)
    adapter.run()
