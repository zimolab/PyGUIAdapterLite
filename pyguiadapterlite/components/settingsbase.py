import json
from typing import Dict, Any, Union

from pyguiadapterlite.components.valuewidget import BaseParameterWidgetConfig


class SettingsMeta(type):
    FIELDS_DEF_NAME = "__setting_fields_def"

    def __new__(metacls, name, bases, namespace):
        __fields_def = {}
        # collect fields definitions from all base classes
        for base in bases:
            if hasattr(base, metacls.FIELDS_DEF_NAME):
                __fields_def.update(getattr(base, metacls.FIELDS_DEF_NAME))
        # collect fields from current class
        __current_fields = set()
        for attr_name, attr_value in namespace.items():
            if attr_name.startswith("_"):
                continue
            if not isinstance(attr_value, BaseParameterWidgetConfig):
                continue
            __fields_def[attr_name] = attr_value
            __current_fields.add(attr_name)

        # hook __init__ method
        __original_init = namespace.get("__init__", None)

        def __init__(self, *args, **kwargs):
            # add fields with its default values to the instance as its attributes
            # so that we use instance.<field_name> to access the current value of the field, and use
            # instance.<field_name> = <new_value> to set a new value for the field.
            # if we use class.<field_name>, it will return the field definition itself instead of its current value
            for field_name, field_def in __fields_def.items():
                object.__setattr__(self, field_name, field_def.default_value)

            if __original_init:
                __original_init(self, *args, **kwargs)

        namespace["__init__"] = __init__

        # create new class with collected fields
        __new_class = super().__new__(metacls, name, bases, namespace)
        setattr(__new_class, metacls.FIELDS_DEF_NAME, __fields_def)
        return __new_class


class SettingsBase(metaclass=SettingsMeta):

    def __init__(self, **kwargs):
        super().__init__()
        if kwargs:
            self.set_values(kwargs)

    @classmethod
    def fields(cls) -> Dict[str, BaseParameterWidgetConfig]:
        result = {}
        for base in cls.__mro__:
            if hasattr(base, SettingsMeta.FIELDS_DEF_NAME) and base != object:
                result.update(getattr(base, SettingsMeta.FIELDS_DEF_NAME))
        return result

    @classmethod
    def default_values(cls) -> Dict[str, Any]:
        result = {}
        for field_name, field_def in cls.fields().items():
            result[field_name] = field_def.default_value
        return result

    def values(self) -> Dict[str, Any]:
        ret = {}
        fields_ = self.__class__.fields()
        for field_name in fields_.keys():
            value = getattr(self, field_name)
            ret[field_name] = value
        return ret

    def set_values(self, values: Dict[str, Any], ignore_unknown_fields=True):
        fields_ = self.__class__.fields()
        for field_name, value in values.items():
            if field_name not in fields_:
                if not ignore_unknown_fields:
                    raise ValueError(f"Unknown field: {field_name}")
                continue
            setattr(self, field_name, value)

    @classmethod
    def new(cls, values: Dict[str, Any], ignore_unknown_fields=True) -> "SettingsBase":
        obj = cls()
        obj.set_values(values, ignore_unknown_fields)
        return obj

    def serialize(self) -> Union[str, bytes]:
        raise NotImplementedError()

    @classmethod
    def deserialize(cls, data: Any, **kwargs) -> "SettingsBase":
        raise NotImplementedError()


class JsonSettingsBase(SettingsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def deserialize(
        cls, data: Union[str, bytes, bytearray], **kwargs
    ) -> "JsonSettingsBase":
        if not isinstance(data, (str, bytes, bytearray)):
            raise TypeError("data must be a string, bytes or bytearray")
        json_obj = json.loads(data, **kwargs)
        if not isinstance(json_obj, dict):
            raise ValueError("invalid JSON data")
        return cls.new(json_obj)

    def serialize(self, ensure_ascii=False, indent=4, **kwargs) -> str:
        json_obj = self.values()
        return json.dumps(
            json_obj,
            ensure_ascii=ensure_ascii,
            indent=indent,
            **kwargs,
        )

    def save(
        self, file_path: str, ensure_ascii=False, indent=4, encoding="utf-8", **kwargs
    ):
        with open(file_path, "w", encoding=encoding) as f:
            f.write(self.serialize(ensure_ascii=ensure_ascii, indent=indent, **kwargs))

    @classmethod
    def load(cls, file_path: str, encoding="utf-8", **kwargs) -> "JsonSettingsBase":
        with open(file_path, "r", encoding=encoding) as f:
            data = f.read()
        return cls.deserialize(data, **kwargs)
