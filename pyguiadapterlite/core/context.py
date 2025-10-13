from concurrent.futures import Future
from typing import Any, Callable, Literal, Optional

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
        result = func(window, *args, **kwargs)
        future.set_result(result)
    except Exception as e:
        future.set_exception(e)


def _run_on_ui_thread(
    func: Callable[[FnExecuteWindow, Future, list, dict], Any], *args, **kwargs
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

    return _run_on_ui_thread(_func)


def is_progress_label_enabled() -> bool:
    def _func(window: FnExecuteWindow, *args, **kwargs):
        _ = args, kwargs  # unused
        return window.is_progress_label_enabled()

    return _run_on_ui_thread(_func)


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


is_function_cancelled = is_cancel_requested
