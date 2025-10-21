import gettext
import locale
import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Optional

from pyguiadapterlite import assets
from pyguiadapterlite.utils import _exception

_DEFAULT_LOCALE_DIR = assets.locales_dir()
_DEFAULT_DOMAIN = "pyguiadapterlite"
_DEFAULT_LOCALE = "en_US"


class I18N:
    def __init__(
        self,
        domain: str = _DEFAULT_DOMAIN,
        localedir: str = _DEFAULT_LOCALE_DIR,
        locale_code: str = _DEFAULT_LOCALE,
    ):
        self._domain = domain
        self._localedir = localedir
        self._current_locale = locale_code
        self._translation = None
        self._fallback_translations = {}

        # 确保目录存在
        if not os.path.exists(localedir):
            os.makedirs(os.path.abspath(localedir), exist_ok=True)

    def set_locale_dir(self, localedir: str) -> None:
        if not os.path.exists(localedir):
            os.makedirs(localedir, exist_ok=True)
        self._localedir = localedir

    def get_locale_dir(self) -> str:
        return self._localedir

    def set_locale(self, locale_code: str) -> None:
        self._current_locale = locale_code
        try:
            self._translation = gettext.translation(
                self._domain,
                localedir=self._localedir,
                languages=[locale_code],
                fallback=True,
            )
            self._translation.install()
        except FileNotFoundError:
            # 如果找不到翻译文件，使用空翻译
            self._translation = gettext.NullTranslations()
            self._translation.install()

    def gettext(self, message: str) -> str:
        if self._translation:
            return self._translation.gettext(message)
        return message

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        if self._translation:
            return self._translation.ngettext(singular, plural, n)
        return singular if n == 1 else plural

    # 简化方法别名
    def _(self, message: str) -> str:
        """gettext 的简写形式"""
        return self.gettext(message)

    def _n(self, singular: str, plural: str, n: int) -> str:
        """ngettext 的简写形式"""
        return self.ngettext(singular, plural, n)


class I18NManager:
    """
    i18n 管理器，支持多个翻译域
    """

    def __init__(self):
        self._domains: Dict[str, I18N] = {}
        self._default_domain = _DEFAULT_DOMAIN

    def add_domain(self, domain: str, localedir: str = _DEFAULT_LOCALE_DIR) -> I18N:
        i18n = I18N(domain, localedir)
        self._domains[domain] = i18n
        return i18n

    def set_locale(self, locale_code: str, domain: str = None) -> None:
        if domain:
            if domain in self._domains:
                self._domains[domain].set_locale(locale_code)
        else:
            for i18n in self._domains.values():
                i18n.set_locale(locale_code)

    def get_domain(self, domain: str = None) -> I18N:
        domain = domain or self._default_domain
        if domain not in self._domains:
            self.add_domain(domain)
        return self._domains[domain]


class SystemLocaleDetector(object):
    def __init__(self):
        self._system = platform.system().lower()

    def detect(self, default: str = _DEFAULT_LOCALE) -> str:
        if self._system == "linux":
            return self._detect_linux() or default
        elif self._system == "darwin":
            return self._detect_macos() or default
        elif self._system == "windows":
            return self._detect_windows() or default
        else:
            return self._detect_other() or default

    def detect_language_code(
        self, fallback_locale: str = _DEFAULT_LOCALE
    ) -> Optional[str]:
        locale_str = self.detect(fallback_locale).strip()
        if locale_str and "_" in locale_str:
            return locale_str.split("_")[0]
        return locale_str or None

    def detect_country_code(
        self, fallback_locale: str = _DEFAULT_LOCALE
    ) -> Optional[str]:
        locale_str = self.detect(fallback_locale)
        if locale_str and "_" in locale_str:
            return locale_str.split("_")[1]
        return None

    @staticmethod
    def _detect_linux() -> Optional[str]:
        # 检查多个环境变量
        env_vars = ["LC_ALL", "LC_CTYPE", "LANG", "LANGUAGE"]
        for var in env_vars:
            value = os.environ.get(var)
            if value and value != "C" and value != "POSIX":
                return value
        # 使用locale命令
        try:
            result = subprocess.run(["locale"], capture_output=True, text=True)
            if result.returncode != 0:
                return None
            for line in result.stdout.split("\n"):
                line = line.strip()
                if line.startswith("LANG=") or line.startswith("LC_CTYPE="):
                    return line.split("=")[1].strip().strip('"')
            return None
        except BaseException as e:
            _exception(e, "failed to detect system locale on Linux")
            return None

    @staticmethod
    def _detect_macos() -> Optional[str]:
        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleLocale"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except BaseException as e:
            _exception(e, "failed to detect system locale on macOS")
            return None

    @staticmethod
    def _detect_windows() -> Optional[str]:
        try:
            import ctypes

            lcid = ctypes.windll.kernel32.GetUserDefaultLCID()
            return locale.windows_locale.get(lcid, None)
        except BaseException as e:
            _exception(e, "failed to detect system locale on Windows")
            return None

    @staticmethod
    def _detect_other() -> Optional[str]:
        try:
            return locale.getdefaultlocale()[0] or None
        except BaseException as e:
            _exception(e, "failed to detect system locale on other system")


# 创建全局实例
_manager = I18NManager()
_default_i18n = _manager.add_domain(_DEFAULT_DOMAIN)
_default_detector = SystemLocaleDetector()


# 便捷函数
def set_locale(locale_code: str):
    """设置当前语言"""
    _default_i18n.set_locale(locale_code)


def set_locale_auto(fallback_locale: str = _DEFAULT_LOCALE):
    """自动设置当前语言"""
    locale_code = _default_detector.detect(fallback_locale)
    _default_i18n.set_locale(locale_code)


def set_locale_dir(localedir: str):
    """设置翻译文件目录"""
    _default_i18n.set_locale_dir(localedir)


def detect_system_locale(fallback: str = _DEFAULT_LOCALE) -> str:
    return _default_detector.detect(fallback)


def detect_system_language_code(
    fallback_locale: str = _DEFAULT_LOCALE,
) -> Optional[str]:
    return _default_detector.detect_language_code(fallback_locale)


def detect_system_country_code(fallback_locale: str = _DEFAULT_LOCALE) -> Optional[str]:
    return _default_detector.detect_country_code(fallback_locale)


def tr_(message: str) -> str:
    """翻译字符串"""
    return _default_i18n.gettext(message)


def ntr_(singular: str, plural: str, n: int) -> str:
    """翻译单复数字符串"""
    return _default_i18n.ngettext(singular, plural, n)


def export_locale_dir(target_dir: str, overwrite: bool = False) -> None:
    """导出翻译文件到指定目录"""
    target_dir = Path(target_dir)
    if target_dir.is_dir() and not overwrite:
        return
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(assets.locales_dir(), target_dir, dirs_exist_ok=True)
