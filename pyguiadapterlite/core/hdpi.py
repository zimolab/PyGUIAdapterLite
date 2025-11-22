"""
Originally written by <Wulian233> (https://github.com/Wulian233/hidpi-tk) with
some modification to fit the needs of this project.

The original code is licensed under the Apache-2.0 license, the original license file
can be found at licenses/hidpi-tk-LICENSE.

"""

import os
import re
from ctypes import pointer, windll, wintypes
from tkinter import Tk, Widget, Toplevel

_dpi_aware_enabled = False
_TK_init = Tk.__init__
_Toplevel_init = Toplevel.__init__
_TK_geometry = Tk.geometry
_Toplevel_geometry = Toplevel.geometry
_Widget_place = Widget.place


# noinspection PyUnresolvedReferences,PyBroadException
def Get_HWND_DPI(window_handle):
    """Get DPI information for a window handle."""
    if os.name == "nt":
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass  # this will fail on Windows Server and maybe early Windows

        DPI100pc = 96  # DPI 96 is 100% scaling
        DPI_type = 0  # MDT_EFFECTIVE_DPI = 0, MDT_ANGULAR_DPI = 1, MDT_RAW_DPI = 2
        winH = wintypes.HWND(window_handle)
        monitorhandle = windll.user32.MonitorFromWindow(
            winH, wintypes.DWORD(2)
        )  # MONITOR_DEFAULTTONEAREST = 2

        X = wintypes.UINT()
        Y = wintypes.UINT()
        try:
            windll.shcore.GetDpiForMonitor(
                monitorhandle, DPI_type, pointer(X), pointer(Y)
            )
            return X.value, Y.value, (X.value + Y.value) / (2 * DPI100pc)
        except Exception:
            return 96, 96, 1  # Assume standard Windows DPI & scaling
    else:
        return None, None, 1


# noinspection PyBroadException
def TkGeometryScale(s, cvtfunc):
    """Scale geometry string based on DPI scaling."""
    try:
        patt = r"(?P<W>\d+)x(?P<H>\d+)\+(?P<X>\d+)\+(?P<Y>\d+)"  # format "WxH+X+Y"
        R = re.compile(patt).match(s)
        if R.span()[1] < len(s) - 1:
            raise Exception()
        G = str(cvtfunc(R.group("W"))) + "x"
        G += str(cvtfunc(R.group("H"))) + "+"
        G += str(cvtfunc(R.group("X"))) + "+"
        G += str(cvtfunc(R.group("Y")))
    except Exception:
        try:
            patt = r"(?P<W>\d+)x(?P<H>\d+)"  # format "WxH"
            R = re.compile(patt).match(s)
            if R.span()[1] < len(s) - 1:
                raise Exception()
            G = str(cvtfunc(R.group("W"))) + "x"
            G += str(cvtfunc(R.group("H")))
        except Exception:
            patt = r"\+(?P<X>\d+)\+(?P<Y>\d+)"  # format "+X+Y"
            R = re.compile(patt).match(s)
            if R.span()[1] < len(s) - 1:
                raise Exception("Incorrect geometry string.")
            G = "+" + str(cvtfunc(R.group("X"))) + "+"
            G += str(cvtfunc(R.group("Y")))
    return G


def fix_scaling(root):
    """Scale fonts on HiDPI displays."""
    import tkinter.font

    scaling = float(root.tk.call("tk", "scaling"))
    if scaling > 1.4:
        for name in tkinter.font.names(root):
            font = tkinter.font.Font(root=root, name=name, exists=True)
            size = int(font["size"])
            if size < 0:
                font["size"] = round(-0.75 * size)


# noinspection PyUnresolvedReferences,PyBroadException
def fix_HiDPI(root):
    """Adjust scaling for HiDPI displays on Windows."""
    if os.name == "nt":
        scale_factor = 1.0
        try:
            # For Windows 8.1 and later
            windll.shcore.SetProcessDpiAwareness(2)
            scale_factor = windll.shcore.GetScaleFactorForDevice(0)
            shcore = True
        except Exception:
            # For Windows older than 8.1
            try:
                windll.user32.SetProcessDPIAware()
                shcore = False
            except Exception:
                return

        if shcore:
            # Set Tk scaling based on Windows DPI settings
            root.tk.call("tk", "scaling", 96 * scale_factor / 100 / 72)

            # Get DPI for the monitor
            win_handle = wintypes.HWND(root.winfo_id())
            monitor_handle = windll.user32.MonitorFromWindow(
                win_handle, 2
            )  # MONITOR_DEFAULTTONEAREST = 2

            x_dpi = wintypes.UINT()
            y_dpi = wintypes.UINT()
            windll.shcore.GetDpiForMonitor(
                monitor_handle, 0, pointer(x_dpi), pointer(y_dpi)
            )  # MDT_EFFECTIVE_DPI = 0

            # Store DPI information in the root window
            root.DPI_X = x_dpi.value
            root.DPI_Y = y_dpi.value
            root.DPI_scaling = (x_dpi.value + y_dpi.value) / (2 * 96)
        else:
            root.DPI_X, root.DPI_Y, root.DPI_scaling = Get_HWND_DPI(root.winfo_id())
    else:
        # Non-Windows systems
        root.DPI_X, root.DPI_Y, root.DPI_scaling = Get_HWND_DPI(root.winfo_id())

    fix_scaling(root)


def _dpi_aware_TK_init(self, *args, **kwargs):
    global _dpi_aware_enabled
    if not _dpi_aware_enabled:
        _TK_init(self, *args, **kwargs)
        return
    _TK_init(self, *args, **kwargs)
    fix_HiDPI(self)
    self.TkScale = lambda v: int(float(v) * self.DPI_scaling)


def _dpi_aware_Toplevel_init(self, *args, **kwargs):
    global _dpi_aware_enabled
    if not _dpi_aware_enabled:
        _Toplevel_init(self, *args, **kwargs)
        return
    _Toplevel_init(self, *args, **kwargs)
    fix_HiDPI(self)
    self.TkScale = lambda v: int(float(v) * self.DPI_scaling)


def _dpi_aware_Tk_geometry(self, s):
    global _dpi_aware_enabled
    """DPI-aware replacement for geometry method"""
    if not _dpi_aware_enabled:
        return _TK_geometry(self, s)
    return self.wm_geometry(TkGeometryScale(s, self.TkScale))


def _dpi_aware_Toplevel_geometry(self, s):
    global _dpi_aware_enabled
    """DPI-aware replacement for geometry method"""
    if not _dpi_aware_enabled:
        return _Toplevel_geometry(self, s)
    return self.wm_geometry(TkGeometryScale(s, self.TkScale))


def _dpi_aware_Widget_place(widget, *args, **kwargs):
    global _dpi_aware_enabled
    """DPI-aware replacement for place method"""
    if not _dpi_aware_enabled:
        return _Widget_place(widget, *args, **kwargs)

    scaled_kwargs = kwargs.copy()
    # Check if the widget has DPI_scaling attribute (it's a DPI-aware window)
    if _dpi_aware_enabled and hasattr(widget.master, "DPI_scaling"):
        for key in ("x", "y", "width", "height"):
            if key in scaled_kwargs:
                scaled_kwargs[key] = int(
                    float(scaled_kwargs[key]) * widget.master.DPI_scaling
                )
    return _Widget_place(widget, *args, **scaled_kwargs)


def set_dpi_aware(enabled):
    global _dpi_aware_enabled
    _dpi_aware_enabled = enabled
    if _dpi_aware_enabled:
        Tk.geometry = _dpi_aware_Tk_geometry
        Toplevel.geometry = _dpi_aware_Toplevel_geometry
        Tk.__init__ = _dpi_aware_TK_init
        Toplevel.__init__ = _dpi_aware_Toplevel_init
        Widget.place = _dpi_aware_Widget_place
    else:
        Tk.geometry = _TK_geometry
        Toplevel.geometry = _Toplevel_geometry
        Tk.__init__ = _TK_init
        Toplevel.__init__ = _Toplevel_init
        Widget.place = _Widget_place
