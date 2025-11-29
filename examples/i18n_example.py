from pathlib import Path

import pyguiadapterlite

# set current locale, now support "en_US"/"zh_CN"/"auto"
pyguiadapterlite.set_locale_code("auto")

# set custom locale directory
pyguiadapterlite.set_locales_dir((Path(__file__).parent / "locales").as_posix())

# export built-in locale files to the custom locale directory
pyguiadapterlite.set_export_locales_dir(True)

from pyguiadapterlite import GUIAdapter


def foo(a: int, b: int):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(foo)
    adapter.run()
