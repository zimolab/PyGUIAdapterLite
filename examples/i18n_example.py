import os
from pathlib import Path


# set current locale to "en_US"
# if this environment variable is not set, the default locale will be automatically detected
os.environ["PYGUIADAPTERLITE_LOCALE"] = "en_US"
# os.environ["PYGUIADAPTERLITE_LOCALE"] = "zh_CN"
# os.environ["PYGUIADAPTERLITE_LOCALE"] = "auto"

# set custom locale directory
# if this environment variable is not set, the built-in locale directory will be used
os.environ["PYGUIADAPTERLITE_LOCALE_DIR"] = (
    Path(__file__).parent / "locales"
).as_posix()

# export built-in locale files to the custom locale directory specified by PYGUIADAPTERLITE_LOCALE_DIR
# the custom locale directory should be empty or non-existent, if not empty, nothing will be exported
os.environ["PYGUIADAPTERLITE_EXPORT_LOCALES"] = "true"


from pyguiadapterlite import GUIAdapter


def foo(a: int, b: int):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run()
