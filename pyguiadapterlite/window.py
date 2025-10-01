import tkinter as tk
from pathlib import Path

from pyguiadapterlite.utils import _warning


class MainWindow(tk.Tk):
    def __init__(
        self,
        size: tuple[int, int] = (800, 600),
        position: tuple[int | None, int | None] = (None, None),
        title: str = "PyGUIAdapterLite",
        icon: str | None = None,
    ):
        super().__init__()

        self.geometry(
            f"{size[0]}x{size[1]}{f'+{position[0]}+{position[1]}' if position[0] and position[1] else ''}"
        )
        self.title(title)
        if icon:
            icon = Path(icon)
            if not icon.is_file():
                _warning(f"icon file `{icon}` not found, using default icon.")
            else:
                self.iconbitmap(icon.as_posix())
