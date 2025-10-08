import dataclasses
from tkinter import Tk, Toplevel, Frame, messagebox, BooleanVar
from tkinter.ttk import Button, Checkbutton
from typing import Union, Optional, Any, cast, Dict

from pyguiadapterlite._messages import (
    MSG_WARNING_TITLE,
    MSG_NO_FUNC_DOC,
    MSG_FUNC_EXEC_WIN_TITLE,
    MSG_FUNC_DOC_TAB_TITLE,
    MSG_FUNC_OUTPUT_TAB_TITLE,
    MSG_EXEC_BUTTON_TEXT,
    MSG_CANCEL_BUTTON_TEXT,
    MSG_CLEAR_BUTTON_TEXT,
    MSG_CLEAR_CHECKBOX_TEXT,
    MSG_FUNC_ERR_DIALOG_TITLE,
    MSG_FUNC_RET_DIALOG_TITLE,
    MSG_FUNC_EXECUTING,
    MSG_FUNC_CANCELLABLE,
    MSG_FUNC_NOT_EXECUTING,
    MSG_EXCEPTION_DURING_EXEC,
    MSG_FUNC_RET_MSG,
)
from pyguiadapterlite.windows.basewindow import BaseWindowConfig, BaseWindow
from pyguiadapterlite.core.context import ParameterError
from pyguiadapterlite.core.fn import FnInfo, BaseFunctionExecutor, ExecuteStateListener
from pyguiadapterlite.windows.fnvalidationwindow import (
    ParameterValidationWindow,
    ParameterValidationWindowConfig,
)
from pyguiadapterlite.components.paramtabview import (
    ParameterGroupTabView,
    DEFAULT_GROUP_NAME,
)
from pyguiadapterlite.components.termview import TermView
from pyguiadapterlite.components.textviewer import TextView, SimpleTextViewer
from pyguiadapterlite.core.threaded import ThreadedExecutor
from pyguiadapterlite.core.ucontext import UContext
from pyguiadapterlite.utils import (
    _warning,
    show_warning,
    print_traceback,
    get_exception_info,
    show_error,
    show_information,
    _info,
)
from pyguiadapterlite.components.valuewidget import InvalidValue


@dataclasses.dataclass(frozen=True)
class FnExecuteWindowConfig(BaseWindowConfig):
    title: str = MSG_FUNC_EXEC_WIN_TITLE
    execute_button_text: str = MSG_EXEC_BUTTON_TEXT
    cancel_button_text: str = MSG_CANCEL_BUTTON_TEXT
    clear_button_text: str = MSG_CLEAR_BUTTON_TEXT
    clear_button_visible: bool = True
    clear_checkbox_text: str = MSG_CLEAR_CHECKBOX_TEXT
    clear_checkbox_visible: bool = True
    clear_checkbox_checked: bool = True
    default_parameter_group_name: str = DEFAULT_GROUP_NAME
    document_tab: bool = True
    document_tab_title: str = MSG_FUNC_DOC_TAB_TITLE
    document_font: tuple = ("Arial", 12)
    output_tab_title: str = MSG_FUNC_OUTPUT_TAB_TITLE
    output_font: tuple = ("Consolas", 12)
    output_background: str = "black"
    output_foreground: str = "white"
    enable_output_default_menu: bool = True
    disable_widgets_on_execute: bool = False
    print_function_result: bool = True
    show_function_result: bool = True
    print_function_error: bool = True
    show_function_error: bool = True
    function_error_traceback: bool = True
    error_dialog_title: str = MSG_FUNC_ERR_DIALOG_TITLE
    result_dialog_title: str = MSG_FUNC_RET_DIALOG_TITLE
    parameter_error_message: str = "{}: {}"
    """`ParameterError`类型异常的消息模板，模板第一个变量（`{}`）为`参数名称`，第二个变量(`{}`)为`异常的消息（message）`。"""
    function_result_message: str = MSG_FUNC_RET_MSG
    """函数调用结果的消息模板，在模板中可以使用模板变量（`{}`）来捕获函数的返回值。"""
    function_error_message: str = "{}: {}\n"
    """函数异常或错误的消息模板，模板第一个变量（`{}`）为`异常的类型`，第二个变量(`{}`)为`异常的消息（message）`。"""
    function_executing_message: str = MSG_FUNC_EXECUTING
    """提示消息，用以提示“函数正在执行”。"""
    uncancelable_function_message: str = MSG_FUNC_CANCELLABLE
    """提示消息，用以提示“当前函数为不可取消的函数”。"""
    function_not_executing_message: str = MSG_FUNC_NOT_EXECUTING
    """提示消息，用以提示“当前函数未处于执行状态”。"""


class MainArea(ParameterGroupTabView):

    _DOCUMENT_TAB_ID = "__document__"
    _OUTPUT_TAB_ID = "__output__"

    def __init__(self, parent_window: "FnExecuteWindow", **kwargs):
        self._parent_window = parent_window
        self._fn_info = self._parent_window.fn_info
        self._config = self._parent_window.config
        super().__init__(
            parent_window.parent,
            default_group_name=self._config.default_parameter_group_name,
            **kwargs,
        )

        self._document_view: Optional[TextView] = None
        self._output_view: Optional[TermView] = None

        self._create_parameter_group(DEFAULT_GROUP_NAME)
        self._add_function_parameters()
        self._create_document_tab()
        self._create_output_tab()

    @property
    def output_view(self) -> Optional[TermView]:
        return self._output_view

    def _add_function_parameters(self):
        for name, parameter_config in self._fn_info.parameter_configs.items():
            self.add_parameter(name, parameter_config)

    def _create_document_tab(self):
        if self._config.document_tab and self._fn_info.document.strip():
            document_frame = Frame(self._notebook)

            self._document_view = TextView(
                document_frame, font=self._config.document_font
            )
            self._document_view.set_text(self._fn_info.document)
            self._document_view.pack(fill="both", expand=True)
            self.add_tab(
                tab_id=self.__class__._DOCUMENT_TAB_ID,
                tab_name=self._config.document_tab_title,
                content=document_frame,
            )

    def _create_output_tab(self):
        terminal_frame = Frame(self._notebook)
        self._output_view = TermView(
            terminal_frame,
            font=self._config.output_font,
            default_context_menu=self._config.enable_output_default_menu,
            background=self._config.output_background,
            foreground=self._config.output_foreground,
        )
        self._output_view.pack(fill="both", expand=True)
        self.add_tab(
            tab_id=self.__class__._OUTPUT_TAB_ID,
            tab_name=self._config.output_tab_title,
            content=terminal_frame,
        )

    def show_document_tab(self):
        if self._document_view:
            self.set_current_tab(self.__class__._DOCUMENT_TAB_ID)

    def show_output_tab(self):
        if self._output_view:
            self.set_current_tab(self.__class__._OUTPUT_TAB_ID)


class BottomArea(Frame):
    def __init__(self, parent_window: "FnExecuteWindow", **kwargs):

        self._parent_window = parent_window
        self._config = parent_window.config
        self._fn_info = self._parent_window.fn_info

        self._execute_button: Optional[Button] = None
        self._cancel_button: Optional[Button] = None
        self._clear_button: Optional[Button] = None
        self._clear_checkbox: Optional[Checkbutton] = None

        super().__init__(parent_window.parent, **kwargs)

        self._create_controls()

    def _create_controls(self):
        self._execute_button = Button(
            self,
            text=self._config.execute_button_text,
            command=self._parent_window.on_execute,
        )
        self._execute_button.pack(side="left", padx=5, pady=5)
        self._clear_button = Button(
            self,
            text=self._config.clear_button_text,
            command=self._parent_window.on_clear_output,
            state="disabled" if not self._config.clear_button_visible else "normal",
        )
        self._clear_button.pack(side="left", padx=5, pady=5)
        self._cancel_button = Button(
            self,
            text=self._config.cancel_button_text,
            command=self._parent_window.on_cancel,
            state="normal" if self._fn_info.cancelable else "disabled",
        )
        self._cancel_button.pack(side="left", padx=5, pady=5)
        if self._config.clear_checkbox_visible:
            self._clear_checkbox = Checkbutton(
                self,
                text=self._config.clear_checkbox_text,
                variable=self._parent_window.clear_output_on_execute,
            )
            self._clear_checkbox.pack(side="left", padx=5, pady=5)

    def set_execute_button_state(self, enabled: bool):
        self._execute_button.config(state="normal" if enabled else "disabled")

    def set_cancel_button_state(self, enabled: bool):
        self._cancel_button.config(state="normal" if enabled else "disabled")

    def set_clear_button_state(self, enabled: bool):
        self._clear_button.config(state="normal" if enabled else "disabled")


class FnExecuteWindow(BaseWindow, ExecuteStateListener):
    def __init__(
        self,
        parent: Union[Tk, Toplevel],
        fn_info: FnInfo,
    ):
        config = fn_info.window_config or FnExecuteWindowConfig()
        self._fn_info = fn_info
        self._main_area: Optional[MainArea] = None
        self._bottom_area: Optional[BottomArea] = None

        self.clear_output_on_execute = BooleanVar(value=config.clear_checkbox_checked)
        self._executor: Optional[BaseFunctionExecutor] = None

        self._param_validation_win_parent: Optional[Toplevel] = None
        self._param_validation_win: Optional[ParameterValidationWindow] = None

        super().__init__(parent, config or FnExecuteWindowConfig())

        executor_cls = fn_info.executor or ThreadedExecutor
        self._executor = executor_cls(listener=self)

        UContext.execute_window_created(self)
        _info(f"execute window created(fn={fn_info.fn_name})")

    @property
    def config(self) -> FnExecuteWindowConfig:
        return cast(FnExecuteWindowConfig, super().config)

    @property
    def fn_info(self) -> FnInfo:
        return self._fn_info

    @property
    def main_area(self) -> MainArea:
        return self._main_area

    @property
    def output_view(self) -> TermView:
        return self._main_area.output_view

    @property
    def bottom_area(self) -> BottomArea:
        return self._bottom_area

    def create_main_area(self) -> Any:
        self._main_area = MainArea(self)
        self._main_area.pack(side="top", fill="both", padx=5, pady=5, expand=True)

    def create_bottom_area(self) -> Any:
        bottom_area = BottomArea(self)
        bottom_area.pack(side="bottom", fill="x", padx=5, pady=(5, 2), expand=False)
        self._bottom_area = bottom_area

    def _build_parameter_groups(self):
        parameter_configs = self._fn_info.parameter_configs
        for parameter_name, parameter_config in parameter_configs.items():
            self._main_area.add_parameter(parameter_name, parameter_config)

    def show_function_document(self):
        document = self._fn_info.document
        if not document:
            _warning(MSG_NO_FUNC_DOC)
            messagebox.showwarning(MSG_WARNING_TITLE, MSG_NO_FUNC_DOC)
            return
        doc_viewer = SimpleTextViewer(
            self.parent,
            title=self.config.document_tab_title,
            font=self.config.document_font,
        )
        doc_viewer.set_text(document)
        doc_viewer.show()

    def print(self, *messages: str, sep: str = " ", end: str = "\n"):
        for message in messages:
            self._main_area.output_view.write(f"{message}{sep}")
        if end:
            self._main_area.output_view.write(end)

    def before_execute(self, fn_info: "FnInfo", arguments: Dict[str, Any]) -> None:
        super().before_execute(fn_info, arguments)
        # 切换到输出tab页，方便查看执行结果
        self._main_area.show_output_tab()
        # 切换按钮状态
        self._bottom_area.set_execute_button_state(False)
        self._bottom_area.set_cancel_button_state(self._fn_info.cancelable)
        # self._bottom_area.set_clear_button_state(False)
        # 清理输出
        if self.clear_output_on_execute.get():
            self._main_area.output_view.clear()

    def on_execute_start(self, fn_info: "FnInfo", arguments: Dict[str, Any]) -> None:
        super().on_execute_start(fn_info, arguments)

    def on_execute_finish(
        self,
        fn_info: "FnInfo",
        arguments: Dict[str, Any],
        return_value: Any,
        exception: Optional[BaseException],
    ) -> None:
        super().on_execute_finish(fn_info, arguments, return_value, exception)
        # 函数执行完毕，恢复按钮状态
        self._bottom_area.set_execute_button_state(True)
        self._bottom_area.set_cancel_button_state(False)
        # self._bottom_area.set_clear_button_state(True)
        UContext.current_thread_finished()
        if exception:
            self._handle_function_exception(exception)
        else:
            self._handle_function_result(return_value)

    def on_close(self):
        if self._executor.is_executing:
            show_warning(self.config.function_executing_message)
            return False
        self._close_param_validation_win()
        UContext.execute_window_closed()
        _info(f"execute window closed(fn={self.fn_info.fn_name})")
        return super().on_close()

    def on_execute(self):
        if self._executor.is_executing:
            show_warning(self.config.function_executing_message)
            return
        self._close_param_validation_win()
        parameter_values = self.get_parameter_values()
        if not self.validate_parameter_values(parameter_values):
            return
        self._executor.execute(fn_info=self._fn_info, arguments=parameter_values)

    def on_cancel(self):
        if not self._fn_info.cancelable:
            show_warning(self.config.uncancelable_function_message)
            return
        if not self._executor.is_executing:
            show_warning(self.config.function_not_executing_message)
            return
        self._executor.try_cancel()

    def on_clear_output(self):
        self._close_param_validation_win()
        self._main_area.output_view.clear()

    def get_parameter_values(self) -> Dict[str, Any]:
        parameter_values = self._main_area.get_parameter_values()
        return parameter_values

    def set_parameter_values(self, values: Dict[str, Any]):
        ret = self._main_area.update_parameter_values(values)
        return ret

    def validate_parameter_values(
        self, param_values: Dict[str, Union[Any, InvalidValue]]
    ) -> bool:
        param_values = param_values.copy()
        validation_errors = {}
        for param_name, value in param_values.items():
            if isinstance(value, InvalidValue):
                invalid_msg = value.msg or value.exception
                label = self._get_label_for_parameter(param_name)
                validation_errors[param_name] = (label, str(invalid_msg))

        if self._fn_info.parameters_validator:
            result = self._fn_info.parameters_validator(
                self._fn_info.fn_name, **param_values
            )
            if result:
                for param_name, error in result.items():
                    if error:
                        label = self._get_label_for_parameter(param_name)
                        validation_errors[param_name] = (label, error)

        del param_values

        if validation_errors:
            self._close_param_validation_win()
            self._param_validation_win_parent = Toplevel(self._parent)
            self._param_validation_win = ParameterValidationWindow(
                self._param_validation_win_parent,
                validation_errors,
                config=ParameterValidationWindowConfig(font=self.config.document_font),
            )
            self._param_validation_win.set_on_close_handler(
                self._on_param_validation_win_close
            )
            self._param_validation_win.set_item_clicked_handler(
                self._on_param_validation_win_item_clicked
            )

        if not validation_errors:
            return True
        return False

    def _get_label_for_parameter(self, fn_name: str) -> str:
        for fn_name1, config in self._fn_info.parameter_configs.items():
            if fn_name == fn_name1:
                return config.label or fn_name
        return fn_name

    def _handle_function_result(self, return_value: Any):
        if not (self.config.show_function_result or self.config.print_function_result):
            return
        config = self.config
        msg = config.function_result_message.format(return_value)
        if config.print_function_result:
            self.print(f"\033[1m\033[92m{msg}\033[0m")
        if config.show_function_result:
            show_information(title=config.result_dialog_title, message=msg)

    def _handle_function_exception(self, exception: BaseException):
        config = self.config
        print_traceback(exception)
        exc_type, exc_msg, exc_tb = get_exception_info(exception)
        exc_output_msg = config.function_error_message.format(exc_type, exc_msg).strip()
        if config.print_function_error:
            self.print(
                f"\033[1m\033[91m{MSG_EXCEPTION_DURING_EXEC}\n"
                f"{exc_output_msg}\033[0m"
            )
            if config.function_error_traceback and exc_tb:
                self.print(f"\033[1m\033[93mTraceback:\n{exc_tb}\033[0m")
        if config.show_function_error:
            show_error(title=config.error_dialog_title, message=exc_output_msg)

        if isinstance(exception, ParameterError):
            self._main_area.show_error_effect(exception.parameter_name)

    def _close_param_validation_win(self):
        if self._param_validation_win:
            self._param_validation_win.on_close()

    def _on_param_validation_win_close(self):
        self._param_validation_win = None
        self._param_validation_win_parent = None

    def _on_param_validation_win_item_clicked(self, param_name: str):
        self._main_area.show_error_effect(param_name)
