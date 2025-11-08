import atexit
import signal
import sys
from pathlib import Path
from threading import Event
from typing import Optional, Callable


class ExitHook(object):
    def __init__(
        self,
        once: bool = True,
        hook_uncaught_exception: bool = True,
        wrap_old_excepthook: bool = True,
        hook_signals: bool = True,
        wrap_old_signal_handlers: bool = True,
    ):
        self._once = once
        self._hook_uncaught_exception = hook_uncaught_exception
        self._wrap_old_excepthook = wrap_old_excepthook
        self._hook_signals = hook_signals
        self._wrap_old_signal_handlers = wrap_old_signal_handlers

        self._callbacks = set()

    def try_hook(self, exit_callback: Callable):
        callback_id = id(exit_callback)
        if callback_id in self._callbacks:
            raise ValueError("exit callback already registered")
        self._callbacks.add(callback_id)

        is_called = Event()
        called_once = self._once

        def wrapped_callback():
            nonlocal is_called
            if called_once and is_called.is_set():
                return
            try:
                exit_callback()
            except Exception as e:
                print(
                    f"exit callback {exit_callback} raised exception: {e}",
                    file=sys.stderr,
                )
            is_called.set()

        atexit.register(wrapped_callback)

        if self._hook_uncaught_exception:
            self._do_hook_uncaught_exception(wrapped_callback)

        if self._hook_signals:
            self._do_hook_signals(wrapped_callback)

    def _do_hook_uncaught_exception(self, callback: Callable):
        old_excepthook = sys.excepthook

        def wrapped_excepthook(type, value, traceback):
            try:
                callback()
            except Exception as e:
                print(
                    f"exit callback {callback} raised exception: {e}",
                    file=sys.stderr,
                )

            if callable(old_excepthook) and self._wrap_old_excepthook:
                old_excepthook(type, value, traceback)
            else:
                sys.__excepthook__(type, value, traceback)

        sys.excepthook = wrapped_excepthook

    def _do_hook_signals(self, callback: Callable):
        old_signal_handlers = {
            signal.SIGINT: signal.getsignal(signal.SIGINT),
            signal.SIGTERM: signal.getsignal(signal.SIGTERM),
        }

        def wrapped_signal_handler(signum, frame):
            try:
                callback()
            except Exception as e:
                print(
                    f"exit callback {callback} raised exception: {e}",
                    file=sys.stderr,
                )
            old_handler = old_signal_handlers.get(signum, None)
            if callable(old_handler) and self._wrap_old_signal_handlers:
                return old_handler(signum, frame)

            sys.exit(128 + signum)

        signal.signal(signal.SIGINT, wrapped_signal_handler)
        signal.signal(signal.SIGTERM, wrapped_signal_handler)


def _is_zipimporter(module_name) -> bool:
    module = sys.modules.get(module_name)
    if not module:
        return False

    if not hasattr(module, "__loader__"):
        return False

    try:
        import zipimport

        if isinstance(module.__loader__, zipimport.zipimporter):
            return True
        return False
    except ImportError:
        return False


def is_in_zipapp():
    print(f"self={sys.argv[0]}")
    print(f"__file__={__file__}")

    if getattr(sys, "frozen", False):
        return False

    if hasattr(sys, "_MEIPASS"):
        return False

    path = Path(sys.argv[0])
    if path.suffix in (".pyz", ".pyzw", ".zip"):
        return True
    return _is_zipimporter(__name__)


def _importlib_path(package: str, path: str) -> Optional[Path]:
    try:
        from importlib.resources import as_file, files

        with as_file(files(package).joinpath(path)) as p:
            return Path(p)
    except ImportError:
        return None


def _pkg_resources_path(package: str, path: str) -> Optional[Path]:
    try:
        import pkg_resources

        return Path(pkg_resources.resource_filename(package, path))

    except (ImportError, BaseException):
        return None


def _dir_path(package: str, path: str) -> Optional[Path]:
    pkg = sys.modules.get(package, None)
    if pkg and hasattr(pkg, "__path__") and pkg.__path__:
        return Path(pkg.__path__[0]) / path
    return None


def package_path(package: str, dir_path: str, *paths):
    base_path = (
        _importlib_path(package, dir_path)
        or _pkg_resources_path(package, dir_path)
        or _dir_path(package, dir_path)
    )
    if not base_path:
        raise RuntimeError(f"cannot find directory {dir_path} in package {package}")
    return base_path.joinpath(*paths)
