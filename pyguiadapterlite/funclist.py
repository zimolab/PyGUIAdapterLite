import dataclasses
from tkinter import Tk, Toplevel, StringVar
from tkinter.ttk import Frame, PanedWindow, Label, Entry, Button
from typing import Any, Union, Optional, cast

from .basicwindow import BasicWindow, BasicWindowConfig
from .listview import ListView
from .textviewer import TextView


@dataclasses.dataclass(frozen=True)
class FunctionListWindowConfig(BasicWindowConfig):
    function_list_title: str = "函数列表"
    document_view_title: str = "函数说明"
    label_text_font: tuple = ("Arial", 11, "bold")
    document_font: tuple = ("Arial", 11)
    search_entry_title: str = "搜索"
    no_match_status_text: str = "未找到匹配项"
    no_match_document_text: str = "未找到匹配项"
    no_document_text: str = "未提供说明文档"
    no_selection_status_text: str = "请选择左侧列表中的项目"
    current_view_status_text: str = "当前查看: "
    select_button_text: str = "选择"


class FunctionListWindow(BasicWindow):

    def __init__(
        self,
        parent: Union[Tk, Toplevel],
        config: Optional[FunctionListWindowConfig] = None,
    ):

        config = config or FunctionListWindowConfig()

        self._doc_view: Optional[TextView] = None
        self._status_bar: Optional[Label] = None
        self._right_frame: Optional[Frame] = None
        self._main_pane: Optional[PanedWindow] = None
        self._search_entry: Optional[Entry] = None
        self._listview: Optional[ListView] = None
        self._left_frame: Optional[Frame] = None
        self._search_var: StringVar = StringVar()
        self._list_data = {
            "Python": "Python 是一种高级编程语言，以其简洁的语法和强大的功能而闻名。\n\n特点：\n- 简单易学\n- 跨平台\n- 丰富的库支持\n- 面向对象\n\n应用领域：\n- Web 开发\n- 数据科学\n- 人工智能\n- 自动化脚本",
            "Tkinter": "Tkinter 是 Python 的标准 GUI 库，用于创建桌面应用程序。\n\n特点：\n- 跨平台\n- 简单易用\n- 丰富的组件\n- 完全免费\n\n主要组件：\n- 按钮 (Button)\n- 标签 (Label)\n- 文本框 (Entry)\n- 列表框 (Listbox)\n- 框架 (Frame)",
            "面向对象编程": "面向对象编程 (OOP) 是一种编程范式，使用对象和类来组织代码。\n\n核心概念：\n- 类 (Class)：对象的蓝图\n- 对象 (Object)：类的实例\n- 继承 (Inheritance)：代码重用机制\n- 封装 (Encapsulation)：数据隐藏\n- 多态 (Polymorphism)：同一接口不同实现",
            "数据结构": "数据结构是计算机存储、组织数据的方式。\n\n常见数据结构：\n- 数组 (Array)\n- 链表 (Linked List)\n- 栈 (Stack)\n- 队列 (Queue)\n- 树 (Tree)\n- 图 (Graph)\n\n选择合适的数据结构可以提高程序效率。",
            "算法": "算法是解决特定问题的一系列步骤。\n\n算法特性：\n- 有穷性\n- 确定性\n- 可行性\n- 输入和输出\n\n常见算法类型：\n- 排序算法\n- 搜索算法\n- 图算法\n- 动态规划",
        }
        super().__init__(parent, config)

    @property
    def config(self) -> FunctionListWindowConfig:
        return cast(FunctionListWindowConfig, super().config)

    def create_main_area(self, **kwargs) -> Any:
        self._main_pane = PanedWindow(self._parent, orient="horizontal")
        self._main_pane.pack(fill="both", expand=True)

    def create_left_area(self, **kwargs) -> Any:
        # 创建左侧框架 - 列表区域
        self._left_frame = Frame(self._main_pane)
        self._main_pane.add(self._left_frame, weight=1)
        # 设置左侧列表面板
        self._setup_left_panel()

    def _setup_left_panel(self):
        """设置左侧列表面板"""
        # 添加标题
        list_label = Label(
            self._left_frame,
            text=self.config.function_list_title,
            font=self.config.label_text_font,
        )
        list_label.pack(pady=(0, 5))

        # 添加搜索框
        self._setup_search_entry()

        # 创建列表框
        self._listview = ListView(self._left_frame)
        self._listview.pack(fill="both", expand=True)
        for item in self._list_data.keys():
            self._listview.append(item)
        # 绑定列表选择事件
        self._listview.set_selection_mode("single")
        self._listview.set_double_click_handler(self._on_list_item_double_click)
        self._listview.bind("<<ListboxSelect>>", self._on_select)

        # 添加按钮
        button_frame = Frame(self._left_frame)
        button_frame.pack(pady=(5, 5))
        select_button = Button(
            button_frame,
            text=self.config.select_button_text,
            command=self._on_select_button_clicked,
        )
        select_button.pack(fill="x")

    def _setup_search_entry(self):
        """设置搜索功能"""
        search_frame = Frame(self._left_frame)
        search_frame.pack(fill="x", pady=(5, 5))

        search_label = Label(search_frame, text=self.config.search_entry_title)
        search_label.pack(side="left", padx=(0, 5))

        self._search_entry = Entry(search_frame, textvariable=self._search_var)
        self._search_entry.pack(side="left", fill="x", expand=True)
        # 绑定搜索事件
        self._search_var.trace("w", self._on_search)

    def create_right_area(self, **kwargs) -> Any:
        self._right_frame = Frame(self._main_pane)
        self._main_pane.add(self._right_frame, weight=2)
        self._setup_right_panel()

    def _setup_right_panel(self):
        """设置右侧文档面板"""
        # 添加标题
        doc_label = Label(
            self._right_frame,
            text=self.config.document_view_title,
            font=self.config.label_text_font,
        )
        doc_label.pack(pady=(0, 5))

        # 创建文档显示区域
        doc_frame = Frame(self._right_frame)
        doc_frame.pack(fill="both", expand=True)

        # 创建文档显示控件
        self._doc_view = TextView(
            doc_frame, font=self.config.document_font, wrap="word"
        )
        self._doc_view.pack(side="left", fill="both", expand=True)

        # 添加状态栏
        self._status_bar = Label(
            self._right_frame,
            text=self.config.no_selection_status_text,
            relief="sunken",
            anchor="w",
        )
        self._status_bar.pack(fill="x", pady=(5, 0))

    def _on_select(self, event):
        _ = event
        """处理列表选择事件"""
        selection = self._listview.curselection()
        if selection:
            index = selection[0]
            func_name = self._listview.get(index)
            # 更新文档显示
            self._update_document(func_name)
            # 更新状态栏
            self._status_bar.config(
                text=f"{self.config.current_view_status_text}{func_name}"
            )

    def _on_search(self, *args):
        _ = args
        """处理搜索事件"""
        search_term = self._search_var.get().lower()
        # 清空列表
        self._listview.delete(0, "end")
        # 根据搜索词过滤并重新填充列表
        for item in self._list_data.keys():
            if search_term in item.lower():
                self._listview.insert("end", item)
        # 如果有匹配项，选中第一个
        if self._listview.size() > 0:
            self._listview.selection_set(0)
            self._on_select(None)
        else:
            self._doc_view.set_text(self.config.no_match_document_text)
            self._status_bar.config(text=self.config.no_match_status_text)

    def _update_status(self, text: str):
        self._status_bar.config(text=text)

    def _on_select_button_clicked(self):
        print("选择按钮被点击了", self._listview.curselection())

    def _on_list_item_double_click(self, listview: ListView, index: int):
        _ = listview, index
        print("列表项被双击了", self._listview.curselection())

    def _update_document(self, func_name: str):
        if not func_name:
            return
        doc_text = self._obtain_document(func_name)
        if not doc_text.strip():
            doc_text = self.config.no_document_text
        self._doc_view.set_text(doc_text)

    def _obtain_document(self, func_name: str) -> str:
        """获取函数说明文档"""
        return self._list_data.get(func_name, "")

    def create_main_menu(self, **kwargs) -> Any:
        pass

    def create_bottom_area(self, **kwargs) -> Any:
        pass

    def create_status_bar(self, **kwargs):
        pass
