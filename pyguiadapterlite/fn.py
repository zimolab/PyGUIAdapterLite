import dataclasses
from abc import abstractmethod
from typing import Callable, Any, Type, Dict, Optional, List

from .valuewidget import BaseParameterWidgetConfig


class ExecuteStateListener(object):
    def before_execute(self, fn_info: "FnInfo", arguments: Dict[str, Any]) -> None:
        pass

    def on_execute_start(self, fn_info: "FnInfo", arguments: Dict[str, Any]) -> None:
        pass

    def on_execute_finish(self, fn_info: "FnInfo", arguments: Dict[str, Any]) -> None:
        pass

    def on_execute_result(
        self, fn_info: "FnInfo", arguments: Dict[str, Any], result: Any
    ) -> None:
        pass

    def on_execute_error(
        self, fn_info: "FnInfo", arguments: Dict[str, Any], exception: BaseException
    ) -> None:
        pass


# noinspection PyAbstractClass
class BaseFunctionExecutor(object):

    def __init__(self, listener: Optional[ExecuteStateListener] = None):
        self._listener = listener

    @property
    def listener(self) -> Optional[ExecuteStateListener]:
        return self._listener

    @abstractmethod
    def execute(self, fn_info: "FnInfo", arguments: Dict[str, Any]):
        pass

    @property
    @abstractmethod
    def is_executing(self) -> bool:
        pass

    @abstractmethod
    def try_cancel(self):
        pass

    @property
    @abstractmethod
    def is_cancelled(self) -> bool:
        pass


@dataclasses.dataclass
class ParameterInfo(object):
    default_value: Any
    type: Type
    typename: str
    type_args: List[Any] = dataclasses.field(default_factory=list)
    description: str = None


@dataclasses.dataclass
class FnInfo(object):
    fn: Callable
    fn_name: str
    display_name: Optional[str] = None
    document: Optional[str] = ""
    icon: Optional[str] = None
    parameters: Dict[str, ParameterInfo] = dataclasses.field(default_factory=dict)
    parameter_configs: Dict[str, BaseParameterWidgetConfig] = dataclasses.field(
        default_factory=dict
    )
    cancelable: bool = False
    executor: Optional[Type[BaseFunctionExecutor]] = None
    capture_system_exit_exception: bool = True
