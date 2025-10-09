from datetime import datetime, date, time
from typing import Union

from pyguiadapterlite.types import (
    StringValueWidget,
    TextValueWidget,
    FloatValueWidget,
    RangedFloatValueWidget,
    ScaleFloatValueWidget,
    ScaleIntValueWidget_tk,
)
from pyguiadapterlite.types.extendtypes import (
    text_t,
    int_r,
    int_s,
    float_r,
    directory_t,
    file_t,
    files_t,
    json_obj_t,
    choice_t,
    choices_t,
    int_slider_t,
    int_dial_t,
    color_tuple_t,
    color_hex_t,
    key_sequence_t,
    string_list_t,
    plain_dict_t,
    color_t,
    path_list_t,
    file_list_t,
    dir_list_t,
    font_t,
    int_quantity_t,
    float_quantity_t,
    string_dict_t,
    paths_t,
    float_s,
    int_ss,
)
from pyguiadapterlite.types.ints.common import IntValueWidget
from pyguiadapterlite.types.ints.ranged import RangedIntValueWidget
from pyguiadapterlite.types.ints.scale import ScaleIntValueWidget
from pyguiadapterlite.types.typenames import TYPE_INT, TYPE_FLOAT, TYPE_STR

PyLiteralType = Union[bool, int, float, bytes, str, list, tuple, dict, set, type(None)]


TYPE_TEXT = text_t.__name__
TYPE_INT_R = int_r.__name__
TYPE_INT_S = int_s.__name__
TYPE_INT_SS = int_ss.__name__
TYPE_FLOAT_R = float_r.__name__
TYPE_FLOAT_S = float_s.__name__
TYPE_DIR_T = directory_t.__name__
TYPE_FILE_T = file_t.__name__
TYPE_FILES_T = files_t.__name__
TYPE_JSON_OBJ_T = json_obj_t.__name__
TYPE_PY_LITERAL = str(PyLiteralType)
TYPE_CHOICE_T = choice_t.__name__
TYPE_CHOICES_T = choices_t.__name__
TYPE_SLIDER_INT_T = int_slider_t.__name__
TYPE_DIAL_INT_T = int_dial_t.__name__
TYPE_DATETIME = datetime.__name__
TYPE_DATE = date.__name__
TYPE_TIME = time.__name__
TYPE_COLOR_TUPLE = color_tuple_t.__name__
TYPE_COLOR_HEX = color_hex_t.__name__
# noinspection SpellCheckingInspection
TYPE_COLOR_T = color_t.__name__
TYPE_KEY_SEQUENCE_T = key_sequence_t.__name__
TYPE_STRING_LIST_T = string_list_t.__name__
TYPE_PLAIN_DICT_T = plain_dict_t.__name__
TYPE_PATH_LIST_T = path_list_t.__name__
TYPE_FILE_LIST_T = file_list_t.__name__
TYPE_DIR_LIST_T = dir_list_t.__name__
TYPE_FONT_T = font_t.__name__
TYPE_INT_QUANTITY = int_quantity_t.__name__
TYPE_FLOAT_QUANTITY = float_quantity_t.__name__
TYPE_STRING_DICT_T = string_dict_t.__name__
TYPE_PATHS_T = paths_t.__name__

BUILTIN_WIDGETS_MAP = {
    TYPE_STR: StringValueWidget,
    TYPE_TEXT: TextValueWidget,
    TYPE_INT: IntValueWidget,
    # TYPE_BOOL: BoolBox,
    TYPE_INT_R: RangedIntValueWidget,
    TYPE_INT_S: ScaleIntValueWidget_tk,
    TYPE_INT_SS: ScaleIntValueWidget,
    TYPE_FLOAT: FloatValueWidget,
    TYPE_FLOAT_R: RangedFloatValueWidget,
    TYPE_FLOAT_S: ScaleFloatValueWidget,
    # TYPE_DIR_T: DirSelect,
    # TYPE_FILE_T: FileSelect,
    # TYPE_FILES_T: MultiFileSelect,
    # TYPE_JSON_OBJ_T: JsonEdit,
    # TYPE_ANY: PyLiteralEdit,
    # TYPING_ANY: PyLiteralEdit,
    # TYPE_PY_LITERAL: PyLiteralEdit,
    # TYPING_UNION: PyLiteralEdit,
    # TYPE_OBJECT: PyLiteralEdit,
    # TYPE_DICT: DictEdit,
    # TYPING_DICT: DictEdit,
    # TYPE_MAPPING: DictEdit,
    # TYPE_MUTABLE_MAPPING: DictEdit,
    # TYPING_TYPED_DICT: DictEdit,
    # TYPE_LIST: ListEdit,
    # TYPING_LIST: ListEdit,
    # TYPE_TUPLE: TupleEdit,
    # TYPING_TUPLE: TupleEdit,
    # TYPE_SET: SetEdit,
    # TYPING_SET: SetEdit,
    # TYPE_MUTABLE_SET: SetEdit,
    # TYPING_LITERAL: ExclusiveChoiceBox,
    # TYPE_CHOICE_T: ChoiceBox,
    # TYPE_CHOICES_T: MultiChoiceBox,
    # TYPE_SLIDER_INT_T: Slider,
    # TYPE_DIAL_INT_T: Dial,
    # TYPE_DATETIME: DateTimeEdit,
    # TYPE_DATE: DateEdit,
    # TYPE_TIME: TimeEdit,
    # TYPE_COLOR_TUPLE: ColorTuplePicker,
    # TYPE_COLOR_HEX: ColorHexPicker,
    # TYPE_QCOLOR: ColorPicker,
    # TYPE_COLOR_T: ColorPicker,
    # TYPE_KEY_SEQUENCE_T: KeySequenceEdit,
    # TYPE_STRING_LIST_T: StringListEdit,
    # TYPE_PLAIN_DICT_T: PlainDictEdit,
    # TYPE_PATH_LIST_T: PathListEdit,
    # TYPE_FILE_LIST_T: FileListEdit,
    # TYPE_DIR_LIST_T: DirectoryListEdit,
    # TYPE_FONT_T: FontSelect,
    # TYPE_INT_QUANTITY: IntQuantityBox,
    # TYPE_FLOAT_QUANTITY: FloatQuantityBox,
    # TYPE_STRING_DICT_T: StringDictEdit,
    # TYPE_PATHS_T: PathsEditor,
}

# noinspection PyProtectedMember
BUILTIN_WIDGETS_MAPPING_RULES = [
    # EnumSelect._enum_type_mapping_rule,
    # DictEdit._dict_mapping_rule,
]
