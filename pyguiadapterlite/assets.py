from importlib import resources
from importlib.resources import as_file
from pathlib import Path

_PACKAGE_NAME = "pyguiadapterlite"
_LOCALES_DIR_NAME = "locales"


def assets_dir(dir_name: str) -> Path:
    with as_file(resources.files(_PACKAGE_NAME).joinpath(dir_name)) as path:
        return path


def locale_dir() -> Path:
    return assets_dir(_LOCALES_DIR_NAME)
