from typing import Any

from pyguiadapterlite.core.ucontext import UContext


class ParameterError(Exception):
    def __init__(self, parameter_name: str, message: str):
        self._parameter_name: str = parameter_name
        self._message: str = message
        super().__init__(message)

    @property
    def parameter_name(self) -> str:
        return self._parameter_name

    @property
    def message(self) -> str:
        return self._message


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


is_function_cancelled = is_cancel_requested
