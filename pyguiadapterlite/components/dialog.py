from tkinter import Toplevel, Tk, Widget, Frame
from tkinter.ttk import Button, Entry, Label
from typing import Union, Any, Optional

from pyguiadapterlite._messages import (
    MSG_DIALOG_BUTTON_OK,
    MSG_DIALOG_BUTTON_CANCEL,
    MSG_DIALOG_INPUT_PROMPT,
)


class BaseDialog(object):
    def __init__(
        self,
        parent: Union[Toplevel, Tk, Widget],
        title: str,
        size: tuple = (300, 200),
        resizable: bool = False,
    ):
        self._parent = parent
        self._title = title
        self._size = size

        self._dialog = Toplevel(self._parent)
        self._dialog.withdraw()
        self._dialog.title(self._title)
        self._dialog.geometry(f"{self._size[0]}x{self._size[1]}")
        self._dialog.resizable(resizable, resizable)
        self._dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)

        self._result: Any = None
        self._is_cancelled = False

        self.on_create_content_area(self._dialog)
        self.on_create_buttons(self._dialog)

        parent_window = parent
        if isinstance(parent, Widget):
            parent_window = parent.winfo_toplevel()

        # 将dialog移动到当前鼠标附近
        # x = parent_window.winfo_pointerx() - self._dialog.winfo_reqwidth() // 2
        # y = parent_window.winfo_pointery() - self._dialog.winfo_reqheight() // 2
        # dialog移动到父窗口中央
        x = (
            parent_window.winfo_rootx()
            + parent_window.winfo_width() // 2
            - self._dialog.winfo_reqwidth() // 2
        )
        y = (
            parent_window.winfo_rooty()
            + parent_window.winfo_height() // 2
            - self._dialog.winfo_reqheight() // 2
        )
        self._dialog.geometry(f"+{x}+{y}")
        self._dialog.deiconify()
        self._dialog.transient(parent_window)
        self._dialog.grab_set()
        self._dialog.wait_window()

    def on_create_content_area(self, dialog: Toplevel):
        raise NotImplementedError()

    def on_create_buttons(self, dialog: Toplevel):
        raise NotImplementedError()

    def is_cancelled(self):
        return self._is_cancelled

    @property
    def result(self) -> Any:
        return self._result

    def on_get_result(self) -> Any:
        raise NotImplementedError()

    def on_ok(self):
        self._result = self.on_get_result()
        self._is_cancelled = False
        self._dialog.destroy()

    def on_cancel(self):
        self._is_cancelled = True
        self._dialog.destroy()


class BaseSimpleDialog(BaseDialog):
    def __init__(
        self,
        parent: Union[Toplevel, Tk, Widget],
        title: str,
        size: tuple = (300, 200),
        resizable: bool = False,
        ok_text: str = MSG_DIALOG_BUTTON_OK,
        cancel_text: str = MSG_DIALOG_BUTTON_CANCEL,
    ):
        self._ok_text = ok_text
        self._cancel_text = cancel_text
        self._content_area: Optional[Frame] = None
        self._buttons_area: Optional[Frame] = None
        self._ok_button: Optional[Button] = None
        self._cancel_button: Optional[Button] = None

        super().__init__(parent, title, size, resizable)

    def on_create_content_area(self, dialog: Toplevel):
        self._content_area = Frame(dialog)
        self._content_area.pack(fill="both", expand=True)
        self._content_area.pack(side="top", fill="both", expand=True)

    def on_create_buttons(self, dialog: Toplevel):
        self._buttons_area = Frame(dialog)
        self._buttons_area.pack(side="bottom", fill="x")
        self._ok_button = Button(
            self._buttons_area, text=self._ok_text, command=self.on_ok
        )
        self._ok_button.pack(side="right", padx=5, pady=5)

        self._cancel_button = Button(
            self._buttons_area, text=self._cancel_text, command=self.on_cancel
        )
        self._cancel_button.pack(side="right", padx=5, pady=5)


class StringInputDialog(BaseSimpleDialog):
    def __init__(
        self,
        parent: Union[Toplevel, Tk, Widget],
        title: str,
        size: tuple = (300, 100),
        resizable: bool = False,
        ok_text: str = MSG_DIALOG_BUTTON_OK,
        cancel_text: str = MSG_DIALOG_BUTTON_CANCEL,
        label_text: str = MSG_DIALOG_INPUT_PROMPT,
        initial_value: str = "",
    ):
        self._label_text = label_text
        self._initial_value = initial_value

        self._input_label: Optional[Label] = None
        self._input_entry: Optional[Entry] = None
        super().__init__(parent, title, size, resizable, ok_text, cancel_text)

    def on_get_result(self) -> str:
        return self._input_entry.get()

    def on_create_content_area(self, dialog: Toplevel):
        super().on_create_content_area(dialog)
        if self._label_text:
            self._input_label = Label(self._content_area, text=self._label_text)
            self._input_label.pack(side="top", fill="x", padx=5, pady=(5, 0))
        self._input_entry = Entry(self._content_area)
        self._input_entry.pack(side="bottom", fill="x", expand=True, padx=5, pady=2)
        self._input_entry.insert(0, self._initial_value)
