# i18n_tools.py
import os
import sys
import subprocess
import argparse
import glob
from pathlib import Path

from .. import assets
from ..assets import tools_dir

_LOCALE_DIR = assets.locales_dir()
_BASENAME = "translations"
_MESSAGE_FILENAME = f"{_BASENAME}.po"
_OUTPUT_FILE = _LOCALE_DIR.joinpath(f"{_BASENAME}.pot")

_EXCLUDE_FILES = ("i18ntools.py", "i18n.py", "msgfmt.py", "pygettext.py")
_KEYWORDS = ("tr_", "ntr_")

GETTEXT_TOOL = tools_dir().joinpath("pygettext.py")
MSGFMT_TOOL = tools_dir().joinpath("msgfmt.py")


def extract_strings(
    source_dirs: list,
    output_file: Path = _OUTPUT_FILE,
    keywords: tuple = _KEYWORDS,
    exclude_files: tuple = _EXCLUDE_FILES,
    verbose: bool = False,
):
    """
    从源代码中提取需要翻译的字符串

    Args:
        source_dirs: 源代码目录列表
        output_file: 输出的 PO 模板文件
        keywords: 要提取的关键字列表
        exclude_files: 要排除的文件列表
        verbose: 是否显示详细信息
    """
    keywords = keywords or _KEYWORDS
    if verbose:
        print(f"将通过以下关键字提取字符串: {keywords}")

    pygettext_path = GETTEXT_TOOL.as_posix()

    if not pygettext_path or not os.path.exists(pygettext_path):
        print("错误: 找不到 pygettext.py 工具")
        print("请确保 Python 安装完整，或者手动指定 pygettext.py 路径")
        return False

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 构建命令
    cmd = [sys.executable, pygettext_path]

    # 添加关键字参数
    for keyword in keywords:
        cmd.extend(["-k", keyword])

    cmd.extend(["-o", output_file])

    # 添加所有 Python 文件
    python_files = []
    for source_dir in source_dirs:
        source_dir = os.path.abspath(source_dir)
        for py_file in glob.glob(
            os.path.join(source_dir, "**", "*.py"), recursive=True
        ):
            if os.path.basename(py_file) in exclude_files:
                if verbose:
                    print(f"排除文件: {py_file}")
                continue
            if verbose:
                print(f"发现待处理文件: {py_file}")
            python_files.append(py_file)

    if not python_files:
        print("警告: 没有找到任何 Python 文件")
        return False

    cmd.extend(python_files)

    try:
        print(f"正在提取字符串到: {output_file}")
        print(f"扫描文件: {len(python_files)} 个 Python 文件")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("字符串提取完成")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"提取字符串失败: {e}")
        print(f"{e.stderr}")
        return False


def init_language(language: str, pot_file: Path = _OUTPUT_FILE):
    """
    初始化新语言的翻译文件

    Args:
        language: 语言代码
        pot_file: PO 模板文件路径
    """
    po_dir = _LOCALE_DIR.joinpath(language, "LC_MESSAGES")
    po_file = po_dir.joinpath(_MESSAGE_FILENAME)

    os.makedirs(po_dir, exist_ok=True)

    if os.path.exists(pot_file):
        # 简单复制 pot 文件为 po 文件
        try:
            with open(pot_file, "r", encoding="utf-8") as f:
                content = f.read()
            # 替换文件头信息
            content = content.replace("charset=CHARSET", "charset=UTF-8")
            content = content.replace("Language: ", f"Language: {language}\n")

            with open(po_file, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"{language} 语言的 PO 文件已创建: {po_file}")
            print("请编辑此文件并添加翻译")
            return True
        except Exception as e:
            print(f"创建 PO 文件失败: {e}")
            return False
    else:
        print(f"模板文件不存在: {pot_file}")
        return False


def compile_translations(locale_dir: Path = _LOCALE_DIR):
    """
    编译 PO 文件为 MO 文件

    Args:
        locale_dir: 本地化文件目录
    """
    msgfmt_path = MSGFMT_TOOL.as_posix()

    if not msgfmt_path or not os.path.exists(msgfmt_path):
        print("错误: 找不到 msgfmt.py 工具")
        print("请确保 Python 安装完整，或者手动指定 msgfmt.py 路径")
        return False

    compiled_count = 0

    for root, dirs, files in os.walk(locale_dir):
        for file in files:
            if file.endswith(".po"):
                po_file = os.path.join(root, file)
                mo_file = po_file.replace(".po", ".mo")
                cmd = [sys.executable, msgfmt_path, "-o", mo_file, po_file]
                try:
                    subprocess.run(cmd, check=True, capture_output=True)
                    print(f"已编译: {mo_file}")
                    compiled_count += 1
                except subprocess.CalledProcessError as e:
                    print(f"编译失败 {po_file}: {e}")
                    if e.stderr:
                        print(f"错误详情: {e.stderr.decode('utf-8', errors='ignore')}")
    if compiled_count == 0:
        print("没有找到任何 PO 文件进行编译")
        return False

    print(f"成功编译 {compiled_count} 个翻译文件")
    return True


def update_translations(pot_file: Path = _OUTPUT_FILE, locale_dir: Path = _LOCALE_DIR):
    """
    更新所有语言的 PO 文件，合并新的翻译字符串

    Args:
        pot_file: PO 模板文件路径
        locale_dir: 本地化文件目录
    """
    if not os.path.exists(pot_file):
        print(f"模板文件不存在: {pot_file}")
        return False

    # 这里可以使用 msgmerge 工具，但为了简化，我们提供一个替代方案
    print("注意: 更新翻译功能需要 msgmerge 工具")
    print("请手动更新 PO 文件，或安装 gettext 工具包")
    return False


def list_languages(locale_dir: Path = _LOCALE_DIR):
    """
    列出所有可用的语言

    Args:
        locale_dir: 本地化文件目录
    """
    if not os.path.exists(locale_dir):
        print(f"本地化目录不存在: {locale_dir}")
        return

    languages = []
    for item in os.listdir(locale_dir):
        lang_dir = os.path.join(locale_dir, item)
        if os.path.isdir(lang_dir):
            lc_messages = os.path.join(lang_dir, "LC_MESSAGES")
            if os.path.exists(lc_messages):
                po_file = os.path.join(lc_messages, f"{_BASENAME}.po")
                mo_file = os.path.join(lc_messages, f"{_BASENAME}.mo")
                has_po = os.path.exists(po_file)
                has_mo = os.path.exists(mo_file)
                status = (
                    "PO+MO"
                    if has_po and has_mo
                    else "PO only" if has_po else "MO only" if has_mo else "no files"
                )
                languages.append((item, status))

    if not languages:
        print("没有找到任何语言")
        return

    print("可用语言:")
    for lang, status in languages:
        print(f"  {lang}: {status}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="i18n 工具 - 使用 Python 内置工具")
    parser.add_argument(
        "action",
        choices=["extract", "init", "compile", "update", "list"],
        help="操作: extract-提取字符串, init-初始化语言, compile-编译翻译, update-更新翻译, list-列出语言",
    )
    parser.add_argument("--language", "-l", help="语言代码 (用于 init 操作)")
    parser.add_argument(
        "--source-dirs",
        "-s",
        nargs="+",
        default=["."],
        help="源代码目录 (用于 extract 操作)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=_OUTPUT_FILE,
        help="输出 POT 文件路径 (用于 extract 操作)",
    )
    parser.add_argument(
        "--keywords",
        "-k",
        nargs="+",
        default=_KEYWORDS,
        help="要提取的翻译关键字",
    )
    parser.add_argument(
        "--locale-dir", "-d", default=_LOCALE_DIR.as_posix(), help="本地化文件目录"
    )

    args = parser.parse_args()

    if args.action == "extract":
        success = extract_strings(args.source_dirs, args.output, args.keywords)
        if success:
            print("✅ 字符串提取完成")
        else:
            print("❌ 字符串提取失败")
            sys.exit(1)

    elif args.action == "init":
        if not args.language:
            print("错误: 请使用 --language 指定语言代码")
            sys.exit(1)
        success = init_language(args.language, args.output)
        if success:
            print("✅ 语言初始化完成")
        else:
            print("❌ 语言初始化失败")
            sys.exit(1)

    elif args.action == "compile":
        success = compile_translations(args.locale_dir)
        if success:
            print("✅ 翻译编译完成")
        else:
            print("❌ 翻译编译失败")
            sys.exit(1)

    elif args.action == "update":
        success = update_translations(args.output, args.locale_dir)
        if success:
            print("✅ 翻译更新完成")
        else:
            print("❌ 翻译更新失败")

    elif args.action == "list":
        list_languages(args.locale_dir)


if __name__ == "__main__":
    main()
