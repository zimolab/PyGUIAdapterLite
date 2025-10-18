#!/usr/bin/env python3
"""
Markdown目录生成器
自动提取Markdown文件中的标题并生成目录(TOC)
修复了会将代码块中的#注释也当作标题进行提取的BUG
"""

import re
import argparse
import sys
from pathlib import Path


class MarkdownTOCGenerator:
    def __init__(self, max_depth=6, min_depth=1, toc_title="## 目录"):
        """
        初始化目录生成器

        Args:
            max_depth: 最大标题深度 (1-6)
            min_depth: 最小标题深度 (1-6)
            toc_title: 目录标题
        """
        self.max_depth = max_depth
        self.min_depth = min_depth
        self.toc_title = toc_title
        self.header_pattern = re.compile(r"^(#{1,6})\s+(.+)$")

    def extract_headers(self, content):
        """从Markdown内容中提取标题，忽略代码块中的内容"""
        headers = []
        lines = content.split("\n")

        in_code_block = False
        code_block_delimiter = None

        for line_num, line in enumerate(lines, 1):
            # 检查是否进入或离开代码块
            stripped_line = line.strip()

            # 检测围栏代码块（以```或~~~开头）
            if stripped_line.startswith("```") or stripped_line.startswith("~~~"):
                if not in_code_block:
                    # 进入代码块
                    in_code_block = True
                    code_block_delimiter = stripped_line[:3]  # 获取前三个字符作为分隔符
                elif stripped_line.startswith(code_block_delimiter):
                    # 离开代码块（使用相同的分隔符）
                    in_code_block = False
                    code_block_delimiter = None
                continue

            # 检测缩进代码块（以4个空格或1个制表符开头）
            if not in_code_block and re.match(r"^( {4,}|\t)", line):
                in_code_block = True
                continue
            elif (
                in_code_block
                and not re.match(r"^( {4,}|\t)", line)
                and line.strip() != ""
            ):
                # 离开缩进代码块（遇到非空行且不以4个空格或制表符开头）
                in_code_block = False

            # 如果当前在代码块中，跳过标题检测
            if in_code_block:
                continue

            # 检测标题
            match = self.header_pattern.match(line.strip())
            if match:
                level = len(match.group(1))  # #的数量就是级别
                title = match.group(2).strip()

                # 检查标题级别是否在指定范围内
                if self.min_depth <= level <= self.max_depth:
                    headers.append(
                        {"level": level, "title": title, "line_num": line_num}
                    )

        return headers

    @staticmethod
    def generate_anchor(title):
        """生成GitHub风格的锚点链接"""
        # GitHub锚点生成规则：小写，空格转横线，移除特殊字符
        anchor = title.lower()
        anchor = re.sub(r"[^\w\s-]", "", anchor)  # 移除非字母数字、空格、横线
        anchor = re.sub(r"[\s-]+", "-", anchor)  # 空格和多个横线转单个横线
        anchor = anchor.strip("-")
        return anchor

    def generate_toc(self, headers):
        """根据标题列表生成目录"""
        if not headers:
            return ""

        toc_lines = [self.toc_title, ""]  # 目录标题和空行

        for header in headers:
            level = header["level"]
            title = header["title"]
            anchor = self.generate_anchor(title)

            # 计算缩进 (每级缩进2个空格)
            indent = "  " * (level - self.min_depth)

            # 生成目录项
            toc_line = f"{indent}- [{title}](#{anchor})"
            toc_lines.append(toc_line)

        toc_lines.append("")  # 最后的空行
        return "\n".join(toc_lines)

    def insert_toc_into_content(self, content, toc, placeholder="<!-- TOC -->"):
        """将目录插入到内容中的指定位置"""
        if placeholder in content:
            # 替换现有的占位符
            return content.replace(placeholder, toc)
        else:
            # 如果没有占位符，插入到第一个标题之后
            lines = content.split("\n")
            for i, line in enumerate(lines):
                # 检查是否在代码块中
                in_code_block = False
                for j in range(i):
                    stripped = lines[j].strip()
                    if stripped.startswith("```") or stripped.startswith("~~~"):
                        in_code_block = not in_code_block

                if not in_code_block and self.header_pattern.match(line.strip()):
                    # 在第一个标题后插入目录
                    return "\n".join(lines[: i + 1] + [""] + [toc] + lines[i + 1 :])

            # 如果没有找到标题，插入到文件开头
            return toc + "\n\n" + content

    def process_file(
        self, input_file, output_file=None, in_place=False, placeholder="<!-- TOC -->"
    ):
        """处理单个Markdown文件"""
        try:
            # 读取输入文件
            with open(input_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 提取标题并生成目录
            headers = self.extract_headers(content)
            toc = self.generate_toc(headers)

            if not headers:
                print(f"警告: 在文件 {input_file} 中未找到标题")
                return False

            # 插入目录到内容中
            new_content = self.insert_toc_into_content(content, toc, placeholder)

            # 确定输出文件
            if in_place:
                output_path = input_file
            elif output_file:
                output_path = output_file
            else:
                # 生成新文件名
                input_path = Path(input_file)
                output_path = (
                    input_path.parent / f"{input_path.stem}_with_toc{input_path.suffix}"
                )
            # 写入输出文件
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"成功生成目录: {output_path}")
            print(f"找到 {len(headers)} 个标题")
            return True
        except Exception as e:
            print(f"处理文件 {input_file} 时出错: {e}")
            return False

    def preview_toc(self, content):
        """预览目录而不写入文件"""
        headers = self.extract_headers(content)
        toc = self.generate_toc(headers)
        return toc


def main():
    parser = argparse.ArgumentParser(
        description="自动为Markdown文件生成目录(TOC)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 为单个文件生成目录并预览
  python mktoc.py README.md --preview

  # 为文件生成目录并原地替换
  python mktoc.py README.md --in-place

  # 指定输出文件
  python mktoc.py input.md -o output.md

  # 处理多个文件
  python mktoc.py *.md --in-place

  # 自定义目录深度范围
  python mktoc.py README.md --min-depth 2 --max-depth 4 --in-place
        """,
    )

    parser.add_argument("files", nargs="+", help="要处理的Markdown文件")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument(
        "-i", "--in-place", action="store_true", help="原地修改文件（默认生成新文件）"
    )
    parser.add_argument("--preview", action="store_true", help="仅预览目录而不写入文件")
    parser.add_argument(
        "--min-depth", type=int, default=1, help="最小标题深度 (默认: 1)"
    )
    parser.add_argument(
        "--max-depth", type=int, default=6, help="最大标题深度 (默认: 6)"
    )
    parser.add_argument(
        "--toc-title", default="## 目录", help='目录标题 (默认: "## 目录")'
    )
    parser.add_argument(
        "--placeholder",
        default="<!-- TOC -->",
        help='目录占位符 (默认: "<!-- TOC -->")',
    )

    args = parser.parse_args()

    # 验证参数
    if not (1 <= args.min_depth <= args.max_depth <= 6):
        print("错误: 标题深度范围应在 1-6 之间，且 min-depth <= max-depth")
        sys.exit(1)

    # 创建生成器实例
    generator = MarkdownTOCGenerator(
        max_depth=args.max_depth, min_depth=args.min_depth, toc_title=args.toc_title
    )

    # 处理文件
    success_count = 0
    for file_path in args.files:
        if not Path(file_path).exists():
            print(f"错误: 文件不存在: {file_path}")
            continue

        if args.preview:
            # 预览模式
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                toc = generator.preview_toc(content)
                print(f"\n{file_path} 的目录预览:")
                print("=" * 50)
                print(toc)
                print("=" * 50)
            except Exception as e:
                print(f"预览文件 {file_path} 时出错: {e}")
        else:
            # 生成目录模式
            if generator.process_file(
                file_path, args.output, args.in_place, args.placeholder
            ):
                success_count += 1

    if not args.preview:
        print(f"\n处理完成: 成功处理 {success_count}/{len(args.files)} 个文件")


if __name__ == "__main__":
    main()
