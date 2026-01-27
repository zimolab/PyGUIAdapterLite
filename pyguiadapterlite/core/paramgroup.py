from pyguiadapterlite.core.fn import ParameterError
from pyguiadapterlite.components.settingsbase import SettingsBase


def group_name_hash(group_name: str) -> str:
    return hex(hash(group_name))[2:]


class ParametersGroupBase(SettingsBase):
    GROUP_NAME = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def raise_parameter_error(self, parameter_name: str, message: str) -> None:
        raise ParameterError(
            f"{group_name_hash(self.GROUP_NAME or self.__class__.__name__)}::{parameter_name}",
            message,
        )
