import hashlib

from pyguiadapterlite.core.fn import ParameterError
from pyguiadapterlite.components.settingsbase import SettingsBase


def group_name_hash(group_name: str) -> str:
    obj = hashlib.md5(group_name.encode("utf-8"))
    return obj.hexdigest()


class ParametersGroupBase(SettingsBase):
    GROUP_NAME = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def raise_parameter_error(self, parameter_name: str, message: str) -> None:
        raise ParameterError(
            f"{group_name_hash(self.GROUP_NAME or self.__class__.__name__)}::{parameter_name}",
            message,
        )
