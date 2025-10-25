import threading
from typing import Any, Dict, Optional

from pyguiadapterlite import FnExecuteWindow, GUIAdapter, uprint


def callback_example(a: int, b: float, c: str, d: bool):
    uprint(f"a: {a}, b: {b}, c: {c}, d: {d}")


def before_execute(
    window: FnExecuteWindow, params: Dict[str, Any]
) -> Optional[Dict[str, Any]]:

    # raise an exception will cancel the execution
    # raise Exception("Execution cancelled by user")

    print(f"Before execute callback, in thread: {threading.current_thread()}")
    print(params)
    params["b"] = 2.0
    params["c"] = "modified"

    # you can modify the parameters before the execution actually starts.
    # the original parameters values dict will be modified, you should return the modified dict.
    # DO IT WITH CAUTION!!! If you don't know what you are doing, better not to modify the parameters.
    return params

    # return None in this callback will cancel the execution.
    # return None


def after_execute(
    window: FnExecuteWindow, result: Any, exception: Optional[BaseException]
):
    print(f"After execute callback, in thread: {threading.current_thread()}")
    print("result:", result)
    print("exception:", exception)
    window.print("After execute callback")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        callback_example,
        before_execute_callback=before_execute,
        after_execute_callback=after_execute,
    )
    adapter.run()
