import dataclasses
import tkinter as tk
from tkinter import Toplevel, Tk, messagebox, ttk
from typing import Union, Any, Tuple

from pyguiadapterlite import (
    BaseWindow,
    BaseWindowConfig,
    FnExecuteWindow,
    Action,
    uprint,
    GUIAdapter,
    Menu,
)


class SettingsFrame(ttk.Frame):
    def __init__(self, parent: "SettingsWindow"):
        super().__init__(parent.parent, padding="10")
        self.parent: "SettingsWindow" = parent

        self.theme_var = tk.StringVar(value="light")
        self.auto_save_var = tk.BooleanVar(value=True)
        self.font_size_var = tk.IntVar(value=12)
        self.language_var = tk.StringVar(value="中文")

        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        """创建所有界面控件"""
        self.title_label = ttk.Label(self, text="设置", font=("Arial", 16, "bold"))

        self.theme_frame = ttk.LabelFrame(self, text="主题设置", padding="5")
        self.light_radio = ttk.Radiobutton(
            self.theme_frame, text="浅色主题", variable=self.theme_var, value="light"
        )
        self.dark_radio = ttk.Radiobutton(
            self.theme_frame, text="深色主题", variable=self.theme_var, value="dark"
        )
        self.auto_radio = ttk.Radiobutton(
            self.theme_frame, text="跟随系统", variable=self.theme_var, value="auto"
        )

        self.general_frame = ttk.LabelFrame(self, text="常规设置", padding="5")
        self.auto_save_check = ttk.Checkbutton(
            self.general_frame, text="自动保存", variable=self.auto_save_var
        )
        self.language_combo = ttk.Combobox(
            self.general_frame,
            textvariable=self.language_var,
            values=["中文", "English", "日本語", "Español"],
            state="readonly",
        )
        ttk.Label(self.general_frame, text="界面语言:").grid(
            row=0, column=0, sticky="w"
        )
        self.language_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        self.font_frame = ttk.LabelFrame(self, text="字体设置", padding="5")
        ttk.Label(self.font_frame, text="字体大小:").grid(row=0, column=0, sticky="w")
        self.font_scale = ttk.Scale(
            self.font_frame,
            from_=8,
            to=24,
            variable=self.font_size_var,
            orient="horizontal",
        )
        self.font_value_label = ttk.Label(self.font_frame, text="12")
        self.font_scale.configure(command=self.update_font_value)

        self.button_frame = ttk.Frame(self)
        self.save_btn = ttk.Button(
            self.button_frame, text="保存设置", command=self.save_settings
        )
        self.cancel_btn = ttk.Button(
            self.button_frame, text="取消", command=self.cancel
        )
        self.reset_btn = ttk.Button(
            self.button_frame, text="恢复默认", command=self.reset_settings
        )

    def setup_layout(self):
        """设置控件布局"""
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.theme_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.light_radio.grid(row=0, column=0, sticky="w", padx=(0, 20))
        self.dark_radio.grid(row=0, column=1, sticky="w", padx=(0, 20))
        self.auto_radio.grid(row=0, column=2, sticky="w")

        self.general_frame.grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10)
        )
        self.auto_save_check.grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(5, 0)
        )
        self.general_frame.columnconfigure(1, weight=1)

        self.font_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        self.font_scale.grid(row=0, column=1, sticky="ew", padx=(10, 10))
        self.font_value_label.grid(row=0, column=2)
        self.font_frame.columnconfigure(1, weight=1)

        self.button_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        self.save_btn.grid(row=0, column=0, padx=(0, 10))
        self.cancel_btn.grid(row=0, column=1, padx=(0, 10))
        self.reset_btn.grid(row=0, column=2)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def update_font_value(self, value):
        """更新字体大小显示"""
        self.font_value_label.config(text=str(int(float(value))))

    def save_settings(self):
        """模拟保存设置"""
        messagebox.showinfo("成功", "设置已保存！", parent=self.parent.parent)
        self.parent.close()

    def cancel(self):
        """取消设置"""
        self.parent.close()

    def reset_settings(self):
        """恢复默认设置"""
        self.theme_var.set("light")
        self.auto_save_var.set(True)
        self.font_size_var.set(12)
        self.language_var.set("中文")
        messagebox.showinfo("提示", "已恢复默认设置", parent=self.parent.parent)


@dataclasses.dataclass(frozen=True)
class SettingsWindowConfig(BaseWindowConfig):
    title: str = "设置"
    size: Tuple[int, int] = (400, 600)
    move_to_center: bool = True


class SettingsWindow(BaseWindow):
    def __init__(self, parent: Union[Tk, Toplevel], config: SettingsWindowConfig):
        self._center_frame = None

        super().__init__(parent, config)

        if config.move_to_center:
            self.move_to_center()

    def create_main_area(self) -> Any:
        self._center_frame = SettingsFrame(self)
        self._center_frame.pack(fill="both", expand=True)

    def on_close(self):
        super().on_close()
        print("SettingsWindow closed")


def on_action_settings_window(window: FnExecuteWindow, action: Action):
    _ = action  # 忽略 action 参数
    settings_window_config = SettingsWindowConfig()
    window.show_sub_window(SettingsWindow, settings_window_config, modal=True)


def foo(arg1: int, arg2: str, arg3: bool):
    uprint("arg1:", arg1, "arg2:", arg2, "arg3:", arg3)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        foo,
        window_menus=[
            Menu("文件", [Action("设置", on_triggered=on_action_settings_window)])
        ],
    )
    adapter.run()
