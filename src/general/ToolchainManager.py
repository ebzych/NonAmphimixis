"""Class that manages and provides toolchains and sysroots"""

from os import makedirs, getlogin
from os.path import exists
from abc import ABC
import yaml
from . import general


class ToolchainManager(ABC):
    """"""

    _config_path: str
    _toolset: list[str]

    @staticmethod
    def _parse_config_file() -> None:
        """Search ~/.config/amphimixis/toolset.yml and parse in __toolset list or create it"""

        makedirs(f"/home/{getlogin()}/.config/amphimixis", exist_ok=True)
        if exists(f"/home/{getlogin()}/.config/amphimixis/toolset.yml"):
            with open(
                f"/home/{getlogin()}/.config/amphimixis/toolset.yml",
                "r",
                encoding="utf-8",
            ) as f:
                ToolchainManager._toolset = yaml.safe_load(f)
                f.close()
        else:
            with open(
                f"/home/{getlogin()}/.config/amphimixis/toolset.yml",
                "w",
                encoding="utf-8",
            ) as f:
                template = {"platforms": None, "compilers": None, "sysroots": None}
                yaml.safe_dump(template, f)

    @staticmethod
    def get_compiler_by_name(name: str) -> str:
        """"""

        raise NotImplementedError

    @staticmethod
    def get_sysroot_by_str(name: str) -> str:
        """"""

        raise NotImplementedError

    @staticmethod
    def add_compiler(machine_name: str, path: str, arch: general.Arch) -> None:
        """"""

        raise NotImplementedError

    @staticmethod
    def add_sysroot(name_machine: str, path: str, arch: general.Arch) -> None:
        """"""

        raise NotImplementedError

    @staticmethod
    def install_to_sysroot(path_to_sysroot: str, *packages: str) -> int:
        """"""

        raise NotImplementedError

    @staticmethod
    def remove_compiler(name: str) -> None:
        """"""

        raise NotImplementedError

    @staticmethod
    def remove_sysroot(name: str) -> None:
        """"""

        raise NotImplementedError
