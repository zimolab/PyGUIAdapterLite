from concurrent.futures import Future
from tkinter import messagebox
from typing import Any, Callable, Literal, Optional

from pyguiadapterlite._messages import (
    MSG_INFO_TITLE,
    MSG_WARNING_TITLE,
    MSG_CRITICAL_TITLE,
    MSG_QUESTION_TITLE,
)
from pyguiadapterlite.components import toast
from pyguiadapterlite.core.ucontext import UContext
from pyguiadapterlite.windows.fnexecwindow import FnExecuteWindow


def is_cancel_requested() -> bool:
    if UContext.current_cancel_event() is not None:
        return UContext.current_cancel_event().is_set()
    return False


def uprint(*messages: Any, sep=" ", end="\n"):
    exec_window = UContext.current_execute_window()
    if not exec_window:
        print(*messages, sep=sep, end=end)
        return
    for message in messages:
        exec_window.output_view.write(f"{message}{sep}")
    if end:
        exec_window.output_view.write(end)


def _call_func(
    func: Callable[[FnExecuteWindow, list, dict], Any],
    window: FnExecuteWindow,
    future: Future,
    *args,
    **kwargs,
):
    try:
        future.set_result(func(window, *args, **kwargs))
    except Exception as e:
        future.set_exception(e)


def _run_ui_on_thread(
    func: Callable[[FnExecuteWindow, list, dict], Any], *args, **kwargs
) -> Any:
    exec_window = UContext.current_execute_window()
    if not exec_window:
        raise RuntimeError("fn execute_window is not set")
    future = Future()
    exec_window.parent.after(0, _call_func, func, exec_window, future, args, kwargs)
    return future.result()


def is_progressbar_enabled() -> bool:
    def _func(window: FnExecuteWindow, *args, **kwargs):
        _ = args, kwargs  # unused
        return window.is_progressbar_enabled()

    return _run_ui_on_thread(_func)


def is_progress_label_enabled() -> bool:
    def _func(window: FnExecuteWindow, *args, **kwargs):
        _ = args, kwargs  # unused
        return window.is_progress_label_enabled()

    return _run_ui_on_thread(_func)


def show_progressbar():
    exec_window = UContext.current_execute_window()
    if not exec_window:
        raise RuntimeError("fn execute_window is not set")
    exec_window.parent.after(0, exec_window.show_progressbar)


def hide_progressbar():
    exec_window = UContext.current_execute_window()
    if not exec_window:
        raise RuntimeError("fn execute_window is not set")
    exec_window.parent.after(0, exec_window.hide_progressbar)


def start_progressbar(
    total: int,
    mode: Literal["determinate", "indeterminate"] = "determinate",
    initial_value: int = 0,
    initial_msg: Optional[str] = "",
):
    exec_window = UContext.current_execute_window()
    if not exec_window:
        raise RuntimeError("fn execute_window is not set")
    exec_window.parent.after(
        0, exec_window.start_progressbar, total, mode, initial_value, initial_msg
    )


def update_progressbar(value: int, msg: Optional[str] = None):
    exec_window = UContext.current_execute_window()
    if not exec_window:
        raise RuntimeError("fn execute_window is not set")
    exec_window.parent.after(0, exec_window.update_progressbar, value, msg)


def stop_progressbar(hide_after_stop: bool = True):
    exec_window = UContext.current_execute_window()
    if not exec_window:
        raise RuntimeError("fn execute_window is not set")
    exec_window.parent.after(0, exec_window.stop_progressbar, hide_after_stop)


def show_toast(
    message: str,
    duration: int = 3000,
    position: Literal["top", "bottom", "center"] = "top",
    background: str = "#323232",
    foreground: str = "#FFFFFF",
    font: tuple = ("Arial", 10),
    pad_x: int = 20,
    pad_y: int = 20,
    alpha: float = 0.0,
):
    exec_window = UContext.current_execute_window()
    if not exec_window:
        raise RuntimeError("fn execute_window is not set")

    def _show_toast(window: FnExecuteWindow):
        t = toast.Toast(window.parent)
        t.show_toast(
            message=message,
            duration=duration,
            position=position,
            background=background,
            foreground=foreground,
            font=font,
            pad_x=pad_x,
            pad_y=pad_y,
            alpha=alpha,
        )

    exec_window.parent.after(0, _show_toast, exec_window)


def show_info_messagebox(
    message: str, title: str = MSG_INFO_TITLE, **messagebox_kwargs
) -> str:
    def _call(window: FnExecuteWindow, *args, **kwargs):
        _ = args, kwargs  # unused
        ret = messagebox.showinfo(
            title=title, message=message, parent=window.parent, **messagebox_kwargs
        )
        return ret

    return _run_ui_on_thread(_call)


def show_warning_messagebox(
    message: str, title: str = MSG_WARNING_TITLE, **messagebox_kwargs
) -> str:
    def _call(window: FnExecuteWindow, *args, **kwargs):
        _ = args, kwargs  # unused
        ret = messagebox.showwarning(
            title=title,
            message=message,
            parent=window.parent,
            **messagebox_kwargs,
        )
        return ret

    return _run_ui_on_thread(_call)


def show_critical_messagebox(
    message: str, title: str = MSG_CRITICAL_TITLE, **messagebox_kwargs
) -> str:
    def _call(window: FnExecuteWindow, *args, **kwargs):
        _ = args, kwargs  # unused
        ret = messagebox.showerror(
            title=title,
            message=message,
            parent=window.parent,
            **messagebox_kwargs,
        )
        return ret

    return _run_ui_on_thread(_call)


show_error_messagebox = show_critical_messagebox


def show_question_messagebox(
    message: str,
    title: str = MSG_QUESTION_TITLE,
    **messagebox_kwargs,
) -> str:
    def _call(window: FnExecuteWindow, *args, **kwargs):
        _ = args, kwargs  # unused
        return messagebox.askquestion(
            title=title, message=message, parent=window.parent, **messagebox_kwargs
        )

    return _run_ui_on_thread(_call)


def show_ok_cancel_messagebox(
    message: str,
    title: str = MSG_QUESTION_TITLE,
    **messagebox_kwargs,
) -> bool:
    def _call(window: FnExecuteWindow, *args, **kwargs):
        _ = args, kwargs  # unused
        ret = messagebox.askokcancel(
            title=title, message=message, parent=window.parent, **messagebox_kwargs
        )
        return ret

    return _run_ui_on_thread(_call)


def show_retry_cancel_messagebox(
    message: str,
    title: str = MSG_QUESTION_TITLE,
    **messagebox_kwargs,
) -> Literal["ok", "retry", "cancel"]:
    def _call(window: FnExecuteWindow, *args, **kwargs):
        _ = args, kwargs  # unused
        ret = messagebox.askretrycancel(
            title=title, message=message, parent=window.parent, **messagebox_kwargs
        )
        return ret

    return _run_ui_on_thread(_call)


def show_yes_no_cancel_messagebox(
    message: str,
    title: str = MSG_QUESTION_TITLE,
    **messagebox_kwargs,
) -> Optional[bool]:
    def _call(window: FnExecuteWindow, *args, **kwargs):
        _ = args, kwargs  # unused
        ret = messagebox.askyesnocancel(
            title=title, message=message, parent=window.parent, **messagebox_kwargs
        )
        return ret

    return _run_ui_on_thread(_call)


def show_yes_no_messagebox(
    message: str,
    title: str = MSG_QUESTION_TITLE,
    **messagebox_kwargs,
) -> bool:
    def _call(window: FnExecuteWindow, *args, **kwargs):
        _ = args, kwargs  # unused
        ret = messagebox.askyesno(
            title=title, message=message, parent=window.parent, **messagebox_kwargs
        )
        return ret

    return _run_ui_on_thread(_call)


# 定义别名
is_function_cancelled = is_cancel_requested
