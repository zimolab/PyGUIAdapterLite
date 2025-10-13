from concurrent.futures import Future
from typing import Any, Callable

from pyguiadapterlite.windows.fnexecwindow import FnExecuteWindow
from pyguiadapterlite.core.ucontext import UContext
from pyguiadapterlite.utils import _error


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


def _run_on_ui_thread(
    func: Callable[[FnExecuteWindow, Future], Any], *args, **kwargs
) -> Any:
    exec_window = UContext.current_execute_window()
    if not exec_window:
        raise RuntimeError("fn execute_window is not set")
    future = Future()


def is_progressbar_enabled() -> bool:
    exec_window = UContext.current_execute_window()
    if not exec_window:
        _error("fn execute_window is not set")
        return False
    future = Future()

    def callback():
        future.set_result(exec_window.is_progressbar_enabled())

    exec_window.parent.after(0, callback)
    return future.result()


is_function_cancelled = is_cancel_requested
