import dataclasses
from abc import abstractmethod, ABCMeta
from pathlib import Path
from tkinter import Tk, Toplevel
from typing import Tuple, Optional, Any, Union

from pyguiadapterlite.components.utils import _warning


class ParameterGroupNameNotAvailableError(Exception):
    pass


@dataclasses.dataclass(frozen=True)
class BaseWindowConfig(object):
    title: str = ""
    icon: Optional[str] = None
    size: Tuple[int, int] = (800, 600)
    position: Tuple[Optional[int], Optional[int]] = (None, None)
    always_on_top: bool = False


class BaseWindow(object, metaclass=ABCMeta):
    def __init__(self, parent: Union[Tk, Toplevel], config: BaseWindowConfig):
        self._parent = parent
        self._config = config

        self._parent.title(config.title)
        if config.icon:
            icon_path = Path(config.icon)
            if icon_path.exists():
                self._parent.iconbitmap(icon_path)
        size = config.size
        position = config.position
        self._parent.geometry(
            f"{size[0]}x{size[1]}{f'+{position[0]}+{position[1]}' if position[0] and position[1] else ''}"
        )
        icon = config.icon
        if icon:
            icon = Path(icon)
            if not icon.is_file():
                _warning(f"icon file `{icon}` not found, using default icon.")
            else:
                self._parent.iconbitmap(icon.as_posix())

        self.create_main_area()
        self.create_left_area()
        self.create_right_area()
        self.create_bottom_area()
        self.create_main_menu()
        self.create_status_bar()

        self._parent.protocol("WM_DELETE_WINDOW", self.on_close)
        self.set_always_on_top(config.always_on_top)

    @property
    def parent(self) -> Union[Tk, Toplevel]:
        return self._parent

    @property
    def config(self) -> BaseWindowConfig:
        return self._config

    @abstractmethod
    def create_main_area(self) -> Any:
        pass

    @abstractmethod
    def create_bottom_area(self) -> Any:
        pass

    @abstractmethod
    def create_left_area(self) -> Any:
        pass

    @abstractmethod
    def create_right_area(self) -> Any:
        pass

    @abstractmethod
    def create_main_menu(self) -> Any:
        pass

    @abstractmethod
    def create_status_bar(self):
        pass

    def move_to_center(self):
        """
        将窗口居中显示（自动获取窗口尺寸）
        """
        self.hide()
        # 更新窗口以确保获取正确的尺寸
        self._parent.update()

        # 获取窗口尺寸
        width = self._parent.winfo_width()
        height = self._parent.winfo_height()

        # 获取屏幕尺寸
        screen_width = self._parent.winfo_screenwidth()
        screen_height = self._parent.winfo_screenheight()

        # 计算位置
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # 设置位置
        self._parent.geometry(f"+{x}+{y}")
        self.show()

    def hide(self):
        self._parent.withdraw()

    def show(self):
        self._parent.deiconify()

    def set_always_on_top(self, on: bool):
        self._parent.wm_attributes("-topmost", on)

    def on_close(self):
        if self._parent:
            self._parent.destroy()
            self._parent = None
