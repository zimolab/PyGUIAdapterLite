import dataclasses
import tkinter as tk
from abc import abstractmethod, ABCMeta
from pathlib import Path
from tkinter import Widget, Frame
from typing import Tuple, Optional, Dict, Any, Generator, Union, Literal

from .listview import ListView
from .scrollarea import ParameterWidgetArea, ParameterNotFound
from .tabview import TabView, TabIdNotFoundError
from .utils import _warning
from .valuewidget import BaseParameterWidgetConfig, InvalidValue


DEFAULT_GROUP_NAME = "Main"


class ParameterGroupNameNotAvailableError(Exception):
    pass


@dataclasses.dataclass(frozen=True)
class BasicWindowConfig(object):
    title: str = "BasicWindow"
    icon: Optional[str] = None
    size: Tuple[int, int] = (800, 600)
    position: Tuple[Optional[int], Optional[int]] = (None, None)


class BasicWindow(object, metaclass=ABCMeta):
    def __init__(self, parent: Union[tk.Tk, tk.Toplevel], config: BasicWindowConfig):
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

    @property
    def parent(self) -> Union[tk.Tk, tk.Toplevel]:
        return self._parent

    @property
    def config(self) -> BasicWindowConfig:
        return self._config

    @abstractmethod
    def create_main_area(self, **kwargs) -> Any:
        pass

    @abstractmethod
    def create_bottom_area(self, **kwargs) -> Any:
        pass

    @abstractmethod
    def create_left_area(self, **kwargs) -> Any:
        pass

    @abstractmethod
    def create_right_area(self, **kwargs) -> Any:
        pass

    @abstractmethod
    def create_main_menu(self, **kwargs) -> Any:
        pass

    @abstractmethod
    def create_status_bar(self, **kwargs):
        pass

    def move_to_center(self):
        """
        将窗口居中显示（自动获取窗口尺寸）
        """
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


class MainArea(TabView):
    def __init__(
        self,
        parent: Union[Widget, tk.Tk],
        default_group_name: str = DEFAULT_GROUP_NAME,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        self._default_group_name = default_group_name

    def _create_parameter_group(self, group_name: str) -> ParameterWidgetArea:
        if not self.has_tab(group_name):
            group_tab = ParameterWidgetArea(None)
            self.add_tab(group_name, group_name, group_tab)
            return group_tab
        tab = self.get_tab(group_name)
        if not isinstance(tab, ParameterWidgetArea):
            raise ValueError(
                f"tab `{group_name}` already exists but is not a ParameterWidgetArea."
            )
        return tab

    def add_tab(self, tab_id: str, tab_name: str, content: Widget, **kwargs) -> None:
        if tab_id == self._default_group_name and (
            not isinstance(content, ParameterWidgetArea)
        ):
            raise ValueError(
                f"tab_id `{self._default_group_name}` is reserved for ParameterWidgetArea."
            )
        return super().add_tab(tab_id, tab_name, content, **kwargs)

    @property
    def parameter_groups(self) -> Generator[Tuple[str, ParameterWidgetArea], Any, None]:
        for tab_id, tab in self._tabs.items():
            if isinstance(tab, ParameterWidgetArea):
                yield tab_id, tab

    def get_parameter_group(self, group_name: str) -> Optional[ParameterWidgetArea]:
        if not self.has_tab(group_name):
            raise TabIdNotFoundError(f"tab `{group_name}` not found.")
        tab = self.get_tab(group_name)
        if not isinstance(tab, ParameterWidgetArea):
            raise ValueError(f"tab `{group_name}` is not a ParameterWidgetArea.")
        return tab

    def remove_parameter_group(self, group_name: str):
        if not self.has_tab(group_name):
            raise TabIdNotFoundError(f"tab `{group_name}` not found.")
        tab = self.get_tab(group_name)
        if not isinstance(tab, ParameterWidgetArea):
            raise ValueError(f"tab `{group_name}` is not a ParameterWidgetArea.")
        self.remove_tab(group_name, destroy_content=True)

    def get_parameter_values_of_group(
        self, group_name: str
    ) -> Optional[Dict[str, Any]]:
        if not self.has_tab(group_name):
            raise None
        tab = self.get_tab(group_name)
        if not isinstance(tab, ParameterWidgetArea):
            raise ValueError(f"tab `{group_name}` is not a ParameterWidgetArea.")
        return tab.get_parameter_values()

    def get_parameter_values(self) -> Dict[str, Union[Any, InvalidValue]]:
        values = {}
        for group_name, group in self.parameter_groups:
            group_values = group.get_parameter_values()
            if group_values:
                values.update(group_values)
        return values

    def update_parameter_values(
        self, values: Dict[str, Any]
    ) -> Dict[str, Union[Any, InvalidValue]]:
        ret = {}
        for group_name, group in self.parameter_groups:
            group_values = group.update_parameter_values(values, ignore_not_exist=True)
            if group_values:
                ret.update(group_values)
        return ret

    def find_parameter_group(
        self, parameter_name: str
    ) -> Optional[ParameterWidgetArea]:
        for group_name, group in self.parameter_groups:
            if group.has_parameter(parameter_name):
                return group
        return None

    def get_parameter_group_name(self, parameter_name: str) -> Optional[str]:
        for group_name, group in self.parameter_groups:
            if group.has_parameter(parameter_name):
                return group_name
        return None

    def has_parameter(self, parameter_name: str) -> bool:
        return bool(self.find_parameter_group(parameter_name))

    def show_error_effect(self, parameter_name: str):
        group = self.find_parameter_group(parameter_name)
        if not group:
            _warning(f"parameter `{parameter_name}` not found.")
            return
        self._notebook.select(group)
        parameter_widget = group.get_parameter_widget(parameter_name)
        if not parameter_widget:
            _warning(f"parameter widget for `{parameter_name}` not found.")
            return
        parameter_widget.start_invalid_value_effect()

    def add_parameter(self, parameter_name: str, config: BaseParameterWidgetConfig):
        group_name = config.group or self._default_group_name
        parameter_group = self._create_parameter_group(group_name)
        parameter_group.add_parameter(parameter_name, config)

    def remove_parameter(self, parameter_name: str):
        group = self.find_parameter_group(parameter_name)
        if not group:
            raise ParameterNotFound(f"parameter `{parameter_name}` not found.")
        group.remove_parameter(parameter_name)

    def clear_parameters(self):
        for group_name, group in self.parameter_groups:
            group.clear_parameters()


class BottomArea(object):
    def __init__(self, parent: Union[Widget, tk.Tk], **kwargs):
        super().__init__()
        self._frame = Frame(parent, **kwargs)

    def real(self) -> Frame:
        return self._frame

    def pack(self, **kwargs):
        self._frame.pack(**kwargs)

    def add_widget(self, widget: Widget, **kwargs):
        widget.master = self._frame
        widget.pack(**kwargs)


@dataclasses.dataclass
class BasicMainWindowConfig:
    size: Tuple[int, int] = (800, 600)
    position: Tuple[Optional[int], Optional[int]] = (None, None)
    title: str = "PyGUIAdapterLite"
    icon: Optional[str] = None
    default_group_name: str = DEFAULT_GROUP_NAME
    document: Optional[str] = None
    document_title: Optional[str] = "Document"
    document_type: Literal["html", "pdf", "text"] = "html"


class BasicMainWindow(object):
    def __init__(
        self,
        parent: Union[tk.Tk, tk.Toplevel],
        config: Optional[BasicMainWindowConfig] = None,
    ):
        config = config or BasicMainWindowConfig()
        self._config = config

        size = config.size
        position = config.position
        title = config.title
        icon = config.icon

        self._parent = parent

        self._parent.geometry(
            f"{size[0]}x{size[1]}{f'+{position[0]}+{position[1]}' if position[0] and position[1] else ''}"
        )
        self._parent.title(title)
        if icon:
            icon = Path(icon)
            if not icon.is_file():
                _warning(f"icon file `{icon}` not found, using default icon.")
            else:
                self._parent.iconbitmap(icon.as_posix())

        self._main_area: Optional[MainArea] = self._create_main_area()
        self._bottom_area: Optional[BottomArea] = self._create_bottom_area()

    @property
    def main_area(self) -> MainArea:
        return self._main_area

    @property
    def bottom_area(self) -> BottomArea:
        return self._bottom_area

    def get_parameter_values(self) -> Dict[str, Union[Any, InvalidValue]]:
        return self._main_area.get_parameter_values()

    def update_parameter_values(
        self, values: Dict[str, Any]
    ) -> Dict[str, Union[Any, InvalidValue]]:
        return self._main_area.update_parameter_values(values)

    def show_document(self):
        pass

    def _create_main_area(self) -> MainArea:
        main_area = MainArea(
            self._parent, default_group_name=self._config.default_group_name
        )
        main_area.pack(fill="both", side="top", padx=5, pady=5, expand=True)
        return main_area

    def _create_bottom_area(self) -> BottomArea:
        bottom_area = BottomArea(self._parent)
        bottom_area.pack(fill="x", side="bottom", padx=5, pady=5, expand=False)
        button1 = tk.Button(
            bottom_area.real(), text="Show Document", command=self.show_document
        )
        button1.pack(side="left")
        return bottom_area


@dataclasses.dataclass(frozen=True)
class BasicListWindowConfig(object):
    size: Tuple[int, int] = (400, 600)
    position: Tuple[Optional[int], Optional[int]] = (None, None)
    title: str = "PyGUIAdapterLite"
    icon: Optional[str] = None


class BasicListWindow(object):
    def __init__(
        self,
        parent: Union[tk.Tk, tk.Toplevel],
        config: Optional[BasicListWindowConfig] = None,
    ):
        config = config or BasicListWindowConfig()
        self._parent = parent
        self._config = config

        size = config.size
        position = config.position
        title = config.title
        icon = config.icon

        self._parent.geometry(
            f"{size[0]}x{size[1]}{f'+{position[0]}+{position[1]}' if position[0] and position[1] else ''}"
        )
        self._parent.title(title)
        if icon:
            icon = Path(icon)
            if not icon.is_file():
                _warning(f"icon file `{icon}` not found, using default icon.")
            else:
                self._parent.iconbitmap(icon.as_posix())

        self._listview = self._create_listview()

    @property
    def listview(self) -> ListView:
        return self._listview

    def _create_listview(self) -> ListView:
        listview = ListView(self._parent)
        listview.pack(fill="both", side="top", padx=5, pady=5, expand=True)
        return listview
