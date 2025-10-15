from tkinter import Toplevel, Tk, Widget, BooleanVar
from tkinter.ttk import Entry, Frame, Checkbutton, Label
from typing import Union, Optional, Any, Dict

from pyguiadapterlite import GUIAdapter, BaseSimpleDialog, uprint, show_custom_dialog


# Step 1: Define a custom dialog class
# The custom dialog class should inherit from BaseDialog/BaseSimpleDialog (the latter is recommended, as it has implemented
# two buttons by default, one for OK and one for Cancel)
# and implement the following methods:
# - on_create_content_area(self, dialog: Toplevel) -> None: create the content area of the dialog
# - on_get_result(self) -> Dict[str, Any]: return the result of the dialog
class LoginForm(BaseSimpleDialog):
    def __init__(
        self,
        parent: Union[Toplevel, Tk, Widget],
        title: str = "Login Info",
        size: tuple = (300, 200),
        resizable: bool = False,
        ok_text: str = "Ok",
        cancel_text: str = "Cancel",
    ):
        self._content_area = None
        self._username_entry: Optional[Entry] = None
        self._password_entry: Optional[Entry] = None
        self._keep_login_checkbutton: Optional[Checkbutton] = None

        self._keep_login: BooleanVar = BooleanVar()

        self._login_info = {"username": "", "password": "", "keep_login": False}

        super().__init__(parent, title, size, resizable, ok_text, cancel_text)

    def on_create_content_area(self, dialog: Toplevel):
        self._content_area = Frame(dialog)
        self._content_area.pack(fill="both", expand=True)

        username_label = Label(self._content_area, text="Username:")
        username_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self._username_entry = Entry(self._content_area)
        self._username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        password_label = Label(self._content_area, text="Password:")
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self._password_entry = Entry(self._content_area, show="*")
        self._password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self._keep_login_checkbutton = Checkbutton(
            self._content_area, text="Keep me logged in", variable=self._keep_login
        )
        self._keep_login_checkbutton.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        self._content_area.grid_columnconfigure(1, weight=1)

    def on_get_result(self) -> Dict[str, Any]:
        self._login_info["username"] = self._username_entry.get()
        self._login_info["password"] = self._password_entry.get()
        self._login_info["keep_login"] = self._keep_login.get()
        return self._login_info


def show_custom_dialog_demo():
    # Step 2: Call the show_custom_dialog function with the custom dialog class as the first argument
    # and any other arguments you want to pass to the dialog constructor as keyword arguments.
    # The function will return the result of the dialog (actually, the result is the return value of the on_get_result() method)
    # or None if the dialog was cancelled.
    login_info = show_custom_dialog(
        LoginForm,
        title="User Login",
        size=(300, 200),
        ok_text="Login",
        cancel_text="Later",
    )
    if not login_info:
        uprint("Login cancelled")
    else:
        uprint(f"Username: {login_info['username']}")
        uprint(f"Password: {login_info['password']}")
        uprint(f"Keep me logged in: {login_info['keep_login']}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(show_custom_dialog_demo)
    adapter.run()
