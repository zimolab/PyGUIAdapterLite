"""
集中管理可翻译的消息字符串
"""

from typing import Optional
from pyguiadapterlite.i18n import I18N


DEFAULT_LOCALE_DIR = ""
DEFAULT_DOMAIN = "pyguiadapterlite"

_messages: Optional["Messages"] = None

_custom_domain: str = DEFAULT_DOMAIN
_custom_locales_dir: str = DEFAULT_LOCALE_DIR
_custom_export_locale: bool = False
_custom_locale_code: str = ""


def set_locale_domain(domain: str) -> None:
    global _custom_domain
    _custom_domain = domain


def set_locales_dir(dir_path: str) -> None:
    global _custom_locales_dir
    _custom_locales_dir = dir_path


def set_export_locales_dir(enabled: bool) -> None:
    global _custom_export_locale
    _custom_export_locale = enabled


def set_locale_code(code: str) -> None:
    global _custom_locale_code
    _custom_locale_code = code


class Messages(object):
    def __init__(self):

        global _custom_domain, _custom_locales_dir, _custom_export_locale, _custom_locale_code

        self._i18n = I18N(
            domain=_custom_domain,
            locale_code=_custom_locale_code,
            localedir=_custom_locales_dir,
            export_locales=_custom_export_locale,
        )

        tr_ = self._i18n.gettext

        self.MSG_OBJ_VALIDATION_WIN_TITLE = tr_("Validation Errors")
        self.MSG_INVALID_KEYS_GROUP_TITLE = tr_("Invalid Values")
        self.MSG_INVALID_KEY_LABEL_TEXT = tr_(
            "The following values are invalid and will not be applied:"
        )
        self.MSG_INVALID_KEY_DETAIL_GROUP_TITLE = tr_("Detail")
        self.MSG_INVALID_KEY_DETAIL_TEMPLATE = tr_("Key:\n  {}\n\nReason:\n  {}")
        self.MSG_OBJ_WIN_CONFIRM_BUTTON_TEXT = tr_("Confirm")
        self.MSG_OBJ_WIN_CANCEL_BUTTON_TEXT = tr_("Cancel")
        self.MSG_OBJ_WIN_TITLE = tr_("Object Editor")
        self.MSG_OBJ_WIN_CONTENT_TITLE = tr_("Fields")

        self.MSG_SETTINGS_WIN_TITLE = tr_("Settings")
        self.MSG_SETTINGS_WIN_CONTENT_TITLE = tr_("Options")
        self.MSG_SETTINGS_WIN_CONFIRM_BUTTON_TEXT = tr_("Save")
        self.MSG_SETTINGS_WIN_CANCEL_BUTTON_TEXT = tr_("Cancel")
        self.MSG_SETTINGS_WIN_RESTORE_DEFAULT_BUTTON_TEXT = tr_("Restore Defaults")
        self.MSG_SETTINGS_WIN_RESTORE_DEFAULT_CONFIRM_MSG = tr_(
            "Are you sure to restore default settings?"
        )

        self.MSG_OBJ_VALIDATION_WIN_TITLE = tr_("Validation Errors")
        self.MSG_INVALID_KEYS_GROUP_TITLE = tr_("Invalid Values")
        self.MSG_INVALID_KEY_LABEL_TEXT = tr_(
            "The following values are invalid and will not be applied:"
        )
        self.MSG_INVALID_KEY_DETAIL_GROUP_TITLE = tr_("Detail")
        self.MSG_INVALID_KEY_DETAIL_TEMPLATE = tr_("Key:\n  {}\n\nReason:\n  {}")
        self.MSG_OBJ_WIN_CONFIRM_BUTTON_TEXT = tr_("Confirm")
        self.MSG_OBJ_WIN_CANCEL_BUTTON_TEXT = tr_("Cancel")
        self.MSG_OBJ_WIN_TITLE = tr_("Object Editor")
        self.MSG_OBJ_WIN_CONTENT_TITLE = tr_("Fields")

        self.MSG_DEFAULT_PARAM_GROUP_NAME = tr_("Main")

        self.MSG_WARNING_TITLE = tr_("Warning")
        self.MSG_ERROR_TITLE = tr_("Error")
        self.MSG_INFO_TITLE = tr_("Information")
        self.MSG_QUESTION_TITLE = tr_("Question")
        self.MSG_CRITICAL_TITLE = tr_("Critical")

        self.MSG_NO_FUNC_DOC = tr_("No documentation provided.")

        self.MSG_COPY = tr_("Copy")
        self.MSG_CUT = tr_("Cut")
        self.MSG_PASTE = tr_("Paste")
        self.MSG_UNDO = tr_("Undo")
        self.MSG_REDO = tr_("Redo")

        self.MSG_BROWSE_BUTTON_TEXT = tr_("Browse")

        self.MSG_SELECT_FILE_DIALOG_TITLE = tr_("Select File")
        self.MSG_OPEN_FILE_DIALOG_TITLE = tr_("Open File")
        self.MSG_SAVE_FILE_DIALOG_TITLE = tr_("Save File")
        self.MSG_SELECT_DIR_DIALOG_TITLE = tr_("Select Directory")
        self.MSG_FILE_FILTER_ALL = tr_("All Files")
        self.MSG_FILE_FILTER_TEXT = tr_("Text Files")

        self.MSG_SELECT_ALL = tr_("Select All")
        self.MSG_CLEAR_OUTPUT = tr_("Clear Output")
        self.MSG_SCROLL_TO_TOP = tr_("Scroll to Top")
        self.MSG_SCROLL_TO_BOTTOM = tr_("Scroll to Bottom")
        self.MSG_SAVE_TO_FILE = tr_("Save to File")
        self.MSG_ZOOMING = tr_("Zoom")
        self.MSG_ZOOM_IN = tr_("Zoom In")
        self.MSG_ZOOM_OUT = tr_("Zoom Out")
        self.MSG_ZOOM_RESET = tr_("Zoom Reset")
        self.MSG_NAVIGATION = tr_("Navigation")
        self.MSG_NAV_TOP = tr_("Top")
        self.MSG_NAV_BOTTOM = tr_("Bottom")
        self.MSG_NAV_PAGE_UP = tr_("Page Up")
        self.MSG_NAV_PAGE_DOWN = tr_("Page Down")
        self.MSG_NAV_HINT = tr_("Arrow Keys/PageUp/PageDown")

        self.MSG_FUNC_EXEC_WIN_TITLE = tr_("Function Execution")
        self.MSG_FUNC_DOC_TAB_TITLE = tr_("Function Document")
        self.MSG_FUNC_OUTPUT_TAB_TITLE = tr_("Function Output")
        self.MSG_EXEC_BUTTON_TEXT = tr_("Execute")
        self.MSG_CANCEL_BUTTON_TEXT = tr_("Cancel")

        self.MSG_CLEAR_BUTTON_TEXT = tr_("Clear Output")
        self.MSG_CLEAR_CHECKBOX_TEXT = tr_("clear output before execution")
        self.MSG_FUNC_ERR_DIALOG_TITLE = tr_("Error")
        self.MSG_FUNC_RET_DIALOG_TITLE = tr_("Result")
        self.MSG_FUNC_EXECUTING = tr_("The function is executing, please wait...")
        self.MSG_FUNC_NOT_EXECUTING = tr_("The function is not executing.")
        self.MSG_FUNC_NOT_CANCELLABLE = tr_("The function is not cancellable.")
        self.MSG_EXCEPTION_DURING_EXEC = tr_(
            "An exception occurred during function execution:"
        )
        self.MSG_FUNC_RET_MSG = tr_("The function returned: {}")

        self.MSG_FUNC_SEL_WIN_TITLE = tr_("Select Function")
        self.MSG_SEL_BUTTON_TEXT = tr_("Select")
        self.MSG_FUNC_LIST_TITLE = tr_("Function List")
        self.MSG_FUNC_DOC_TITLE = tr_("Function Document")
        self.MSG_NO_FUNC_DOC_STATUS = tr_("No documentation provided")
        self.MSG_SEL_FUNC_FIRST = tr_("Select a function first!")
        self.MSG_CURRENT_FUNC_STATUS = tr_("Current function: ")

        self.MSG_PARAM_VALIDATION_WIN_TITLE = tr_("Validation Errors")
        self.MSG_INVALID_PARAMS_GROUP_TITLE = tr_("Parameters")
        self.MSG_INVALID_PARAMS_LABEL_TEXT = tr_(
            "Please check the following parameters:"
        )
        self.MSG_INVALID_PARAM_DETAIL_GROUP_TITLE = tr_("Detail")
        self.MSG_INVALID_PARAM_DETAIL_TEMPLATE = tr_(
            "Parameter:\n  {}\n\nReason:\n  {}"
        )

        self.MSG_DIALOG_BUTTON_OK = tr_("OK")
        self.MSG_DIALOG_BUTTON_CANCEL = tr_("Cancel")
        self.MSG_DIALOG_INPUT_PROMPT = tr_("Input:")
        self.MSG_INPUT_DIALOG_TITLE = tr_("Input")
        self.MSG_INPUT_FILE_PROMPT = tr_("Select a file:")
        self.MSG_INPUT_DIR_PROMPT = tr_("Select a directory:")
        self.MSG_INPUT_PATH_PROMPT = tr_("Select a path:")

        self.MSG_PATH_DIALOG_FILE_BUTTON_TEXT = tr_("File")
        self.MSG_PATH_DIALOG_DIR_BUTTON_TEXT = tr_("Folder")

        self.MSG_ADD_ITEM_DIALOG_TITLE = tr_("Add Item")
        self.MSG_ADD_ITEM_DIALOG_LABEL_TEXT = tr_("Add a new item:")
        self.MSG_EDIT_ITEM_DIALOG_TITLE = tr_("Edit Item")
        self.MSG_EDIT_ITEM_DIALOG_LABEL_TEXT = tr_("Edit the item:")
        self.MSG_DUPLICATE_ITEMS_WARNING = tr_(
            "An item with the same value already exists!"
        )
        self.MSG_MULTIPLE_SELECTION_WARNING = tr_("Please select only one item!")
        self.MSG_EMPTY_STRING_WARNING = tr_("The string to be added cannot be empty!")

        self.MSG_MOVE_UP_BUTTON_TEXT = tr_("↑")
        self.MSG_MOVE_DOWN_BUTTON_TEXT = tr_("↓")
        self.MSG_REMOVE_BUTTON_TEXT = tr_("Remove")
        self.MSG_REMOVE_ALL_BUTTON_TEXT = tr_("Clear")
        self.MSG_EDIT_BUTTON_TEXT = tr_("Edit")
        self.MSG_ADD_BUTTON_TEXT = tr_("Add")
        self.MSG_REMOVE_CONFIRMATION = tr_(
            "Are you sure to remove selected items from the list?"
        )
        self.MSG_REMOVE_ALL_CONFIRMATION = tr_(
            "Are you sure to remove all items from the list?"
        )
        self.MSG_NO_ITEMS_WARNING = tr_("There are no items in the list!")
        self.MSG_NO_SELECTION_WARNING = tr_("No item is selected!")

        self.MSG_ADD_FILE_BUTTON_TEXT = tr_("File")
        self.MSG_ADD_DIR_BUTTON_TEXT = tr_("Folder")
        self.MSG_EDIT_PATH_DIALOG_TITLE = tr_("Edit Path")
        self.MSG_EDIT_PATH_DIALOG_LABEL_TEXT = tr_("Edit the path:")
        self.MSG_ADD_PATH_DIALOG_TITLE = tr_("Add Path")
        self.MSG_ADD_PATH_DIALOG_LABEL_TEXT = tr_("Add a new path:")
        self.MSG_EMPTY_PATH_WARNING = tr_("The path cannot be empty!")
        self.MSG_DUPLICATE_PATH_WARNING = tr_(
            "The path has already been added to the list!"
        )
        self.MSG_NO_PATHS_WARNING = tr_("There are no paths in the list!")
        self.MSG_NO_PATHS_SELECTED_WARNING = tr_("No path is selected!")
        self.MSG_REMOVE_PATH_CONFIRMATION = tr_(
            "Are you sure to remove the selected path from the list?"
        )
        self.MSG_REMOVE_ALL_PATHS_CONFIRMATION = tr_(
            "Are you sure to remove all paths from the list?"
        )

        self.MSG_PARAMS_SERIALIZATION_FAILED = tr_("Failed to serialize parameters!")
        self.MSG_SAVE_PARAMS_FAILED = tr_("Failed to save parameters to file!")
        self.MSG_SAVE_PARAMS_SUCCESS = tr_("Parameters saved successfully!")
        self.MSG_LOAD_PARAMS_FAILED = tr_("Failed to load parameters from file!")
        self.MSG_PARAMS_DESERIALIZATION_FAILED = tr_(
            "Failed to deserialize parameters!"
        )
        self.MSG_SET_PARAMS_FAILED = tr_("Failed to set parameters!")
        self.MSG_INVALID_PARAMS_FOUND = tr_("Invalid parameters found!")
        self.MSG_LOAD_FILE_DIALOG_TITLE = tr_("Load File")
        self.MSG_LOAD_PARAMS_SUCCESS = tr_("Parameters loaded successfully!")
        self.MSG_INVALID_PARAMS_NOT_APPLIED = tr_(
            "The following parameters are invalid and will not be applied:"
        )


def messages() -> "Messages":
    global _messages
    if _messages is None:
        _messages = Messages()
    return _messages
