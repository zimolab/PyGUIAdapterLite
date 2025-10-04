import dataclasses
from tkinter import Tk, Toplevel, Widget, Frame
from tkinter.ttk import Button
from typing import Union, Optional, Any, cast

from .basicwindow import BasicWindowConfig, BasicWindow
from .fn import FnInfo
from .paramtabview import ParameterGroupTabView, DEFAULT_GROUP_NAME
from .termview import TermView
from .textviewer import TextView, SimpleTextViewer
from .utils import _warning


@dataclasses.dataclass(frozen=True)
class ExecWindowConfig(BasicWindowConfig):
    default_group_name: str = DEFAULT_GROUP_NAME
    document_tab: bool = True
    document_tab_name: str = "Function Document"
    document_font: tuple = ("Arial", 12)
    terminal_tab_name: str = "Function Output"
    terminal_font: tuple = ("Consolas", 12)
    terminal_background: str = "black"
    terminal_foreground: str = "white"
    terminal_default_menu: bool = True


class MainArea(ParameterGroupTabView):
    def __init__(
        self,
        parent: Union[Widget, Tk, Toplevel],
        fn_info: FnInfo,
        exec_window_config: ExecWindowConfig,
        **kwargs,
    ):
        self._fn_info = fn_info
        self._exec_window_config = exec_window_config
        super().__init__(
            parent, default_group_name=exec_window_config.default_group_name, **kwargs
        )

        self._document_view: Optional[TextView] = None
        self._terminal_view: Optional[TermView] = None

        self._create_parameter_group(DEFAULT_GROUP_NAME)
        self._add_function_parameters()
        self._create_document_tab()
        self._create_terminal_tab()

    @property
    def terminal_view(self) -> Optional[TermView]:
        return self._terminal_view

    def _add_function_parameters(self):
        for name, parameter_config in self._fn_info.parameter_configs.items():
            self.add_parameter(name, parameter_config)

    def _create_document_tab(self):
        if self._exec_window_config.document_tab and self._fn_info.document.strip():
            document_frame = Frame(self._notebook)

            self._document_view = TextView(
                document_frame, font=self._exec_window_config.document_font
            )
            self._document_view.set_text(self._fn_info.document)
            self._document_view.pack(fill="both", expand=True)
            self.add_tab(
                self._exec_window_config.document_tab_name,
                self._exec_window_config.document_tab_name,
                document_frame,
            )

    def _create_terminal_tab(self):
        terminal_frame = Frame(self._notebook)
        self._terminal_view = TermView(
            terminal_frame,
            font=self._exec_window_config.terminal_font,
            default_context_menu=self._exec_window_config.terminal_default_menu,
            background=self._exec_window_config.terminal_background,
            foreground=self._exec_window_config.terminal_foreground,
        )
        self._terminal_view.pack(fill="both", expand=True)
        self.add_tab(
            self._exec_window_config.terminal_tab_name,
            self._exec_window_config.terminal_tab_name,
            terminal_frame,
        )


class ExecWindow(BasicWindow):
    def __init__(
        self,
        parent: Union[Tk, Toplevel],
        fn_info: FnInfo,
        config: Optional[ExecWindowConfig] = None,
    ):
        self._fn_info = fn_info
        self._main_area: Optional[MainArea] = None
        super().__init__(parent, config or ExecWindowConfig())

    @property
    def config(self) -> ExecWindowConfig:
        return cast(ExecWindowConfig, super().config)

    def create_main_area(self) -> Any:
        self._main_area = MainArea(
            self.parent, fn_info=self._fn_info, exec_window_config=self.config
        )
        self._main_area.pack(side="top", fill="both", padx=5, pady=5, expand=True)

    def create_left_area(self) -> Any:
        pass

    def create_bottom_area(self) -> Any:
        bottom_frame = Frame(self.parent)
        bottom_frame.pack(side="bottom", fill="x", padx=5, pady=2, expand=False)

        button = Button(
            bottom_frame, text="显示函数文档", command=self.show_function_document
        )
        button.pack(side="left")

    def create_right_area(self) -> Any:
        pass

    def create_main_menu(self) -> Any:
        pass

    def create_status_bar(self):
        pass

    def show_function_document(self):
        document = self._fn_info.document
        if not document:
            _warning("function document not provided")
            return
        doc_viewer = SimpleTextViewer(
            self.parent,
            title=self.config.document_tab_name,
            font=self.config.document_font,
        )
        doc_viewer.set_text(document)
        doc_viewer.show()
