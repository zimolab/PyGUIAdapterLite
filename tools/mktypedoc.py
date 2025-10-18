#!/usr/bin/env python3
"""
自动生成内置类型所对应控件、控件配置类、可配置属性的文档
"""
import ast
import dataclasses
import inspect
from dataclasses import MISSING
from pathlib import Path
from typing import Any, Dict, List, Set, Literal

DOCS_TEMPLATE = """
{headings} （{num}）`{typename}` ——> `{conf_class}`

<img src="docs/{typename}_w.png" style="height: auto;width: 100%;" />

默认控件类：[`{widget_class}`]({widget_class_path}#L{widget_class_line})
默认配置类：[`{conf_class}`]({conf_class_path}#L{conf_class_line})
可配置属性：
{props}
"""

import sys

sys.path.append(str(Path(__file__).parent.parent))

from pyguiadapterlite.types.widgetmap import BUILTIN_WIDGETS_MAP


_here = Path(__file__).parent.parent.absolute()


@dataclasses.dataclass
class Attr:
    name: str
    typename: str
    default: Any
    docstring: str


@dataclasses.dataclass
class DataclassInfo:
    class_name: str
    docstring: str
    module: str
    attributes: Dict[str, Attr]


def get_file_path(cls, relative_to=_here):
    path = Path(inspect.getfile(cls))
    if relative_to:
        path = path.relative_to(relative_to)
    return path.as_posix()


def get_source_line(cls):
    return inspect.getsourcelines(cls)[1]


# noinspection PyDataclass
def get_own_fields(cls) -> List[dataclasses.Field]:
    if not dataclasses.is_dataclass(cls):
        raise TypeError(f"{cls.__name__} 不是 dataclass")
    # 获取所有父类的字段集合
    parent_fields: Set[str] = set()
    for base in cls.__bases__:
        if dataclasses.is_dataclass(base):
            # noinspection PyTypeChecker
            for field in dataclasses.fields(base):
                parent_fields.add(field.name)
    # 过滤出当前类自己定义的字段（不在父类中的字段）
    own_fields = []
    for field in dataclasses.fields(cls):
        if field.name not in parent_fields:
            own_fields.append(field)
    return own_fields


def get_dataclass_info(cls):
    if not hasattr(cls, "__dataclass_fields__"):
        raise TypeError(f"{cls.__name__} 不是 dataclass")
    attributes = {}
    class_info = DataclassInfo(
        class_name=cls.__name__,
        docstring=inspect.getdoc(cls),
        module=cls.__module__,
        attributes=attributes,
    )
    for field_obj in get_own_fields(cls):

        default = field_obj.default if field_obj.default is not MISSING else ""

        if default and isinstance(default, str):
            default = f'"{default}"'

        attr = Attr(
            name=field_obj.name,
            typename=getattr(field_obj.type, "__name__", str(field_obj.type)),
            default=default,
            docstring="",
        )
        attributes[field_obj.name] = attr
    get_attr_docstrings(cls, attributes)
    return class_info


def extract_attribute_docstrings(cls) -> Dict[str, str]:
    try:
        # 获取类的源代码
        source = inspect.getsource(cls)
        # 解析为 AST
        tree = ast.parse(source)
        # 查找类定义
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == cls.__name__:
                return _extract_docstrings_from_class(node)
    except (TypeError, OSError, SyntaxError) as e:
        print(f"解析类 {cls.__name__} 时出错: {e}")
    return {}


def _extract_docstrings_from_class(class_node):
    """从类节点中提取文档字符串"""
    docstrings = {}
    i = 0
    while i < len(class_node.body):
        node = class_node.body[i]

        # 查找带类型注解的赋值（字段定义）
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            field_name = node.target.id

            # 检查下一个节点是否是字符串表达式（文档字符串）
            if i + 1 < len(class_node.body):
                next_node = class_node.body[i + 1]
                if (
                    isinstance(next_node, ast.Expr)
                    and isinstance(next_node.value, ast.Constant)
                    and isinstance(next_node.value.value, str)
                ):

                    docstrings[field_name] = next_node.value.value
                    i += 1  # 跳过文档字符串节点
        i += 1
    return docstrings


def get_attr_docstrings(cls, attrs: Dict[str, Attr]):
    docstrings = extract_attribute_docstrings(cls)
    for name, docstr in docstrings.items():
        if name in attrs:
            attrs[name].docstring = docstr


def to_markdown_table(
    attrs: Dict[str, Attr],
    sort_by_name: bool = True,
    max_description_length: int = None,
) -> str:
    if not attrs:
        return ""

    # 准备表头
    headers = ["字段名", "类型", "默认值", "描述"]

    # 处理属性列表
    attr_items = list(attrs.items())
    if sort_by_name:
        attr_items.sort(key=lambda x: x[0])

    # 构建表格行
    rows = []
    for attr_name, attr in attr_items:
        # 处理默认值的显示
        default_str = str(attr.default)
        if default_str.strip():
            default_str = f"`{default_str}`"
        else:
            default_str = '""'
        type_name = attr.typename
        if type_name:
            type_name = f"`{type_name}`"
        # 处理描述字段
        description = attr.docstring
        if max_description_length and len(description) > max_description_length:
            description = description[: max_description_length - 3] + "..."
        # 构建行
        row = [attr_name, type_name, default_str, description]
        rows.append(row)

    # 计算每列的最大宽度
    col_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    # 构建表格
    table_lines = []
    # 表头
    header_line = (
        "| "
        + " | ".join(header.ljust(width) for header, width in zip(headers, col_widths))
        + " |"
    )
    table_lines.append(header_line)
    # 分隔线
    separator_line = (
        "| " + " | ".join(":" + "-" * (width - 1) for width in col_widths) + " |"
    )
    table_lines.append(separator_line)
    # 数据行
    for row in rows:
        row_line = (
            "| "
            + " | ".join(str(cell).ljust(width) for cell, width in zip(row, col_widths))
            + " |"
        )
        table_lines.append(row_line)

    return "\n".join(table_lines)


def make_type_doc_for_class(current_num, typename, widget_class, header_level=5) -> str:
    conf_class = widget_class.ConfigClass
    conf_class_path = get_file_path(conf_class)
    conf_class_line = get_source_line(conf_class)
    widget_class_path = get_file_path(widget_class)
    widget_class_line = get_source_line(widget_class)
    attrs = get_dataclass_info(conf_class).attributes
    attrs_table = to_markdown_table(attrs)
    headings = "#" * header_level
    return DOCS_TEMPLATE.format(
        num=current_num,
        headings=headings,
        typename=typename,
        conf_class=conf_class.__name__,
        conf_class_path=conf_class_path,
        conf_class_line=conf_class_line,
        widget_class=widget_class.__name__,
        widget_class_path=widget_class_path,
        widget_class_line=widget_class_line,
        props=attrs_table,
    ).strip()


def make_type_doc(action: Literal["preview", "save"] = "preview", output_file=None):
    current_num = 1
    sections = []
    for typename, widget_class in BUILTIN_WIDGETS_MAP.items():
        sections.append(make_type_doc_for_class(current_num, typename, widget_class))
        current_num += 1
    content = "\r\n\r\n\r\n".join(sections)
    if action == "preview":
        print(content)
    elif action == "save":
        if not output_file:
            raise ValueError("未指定输出文件路径")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        raise ValueError(f"不支持的操作: {action}")


def main():
    # 编写命令行程序
    import argparse

    parser = argparse.ArgumentParser(description="生成内置类型文档")
    parser.add_argument(
        "--action",
        choices=["preview", "save"],
        default="preview",
        help="预览或保存文档",
    )
    parser.add_argument(
        "--output-file",
        help="保存文档的文件路径",
    )
    args = parser.parse_args()
    make_type_doc(args.action, args.output_file)


if __name__ == "__main__":
    main()
