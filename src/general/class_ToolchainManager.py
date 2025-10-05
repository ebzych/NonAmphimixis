"""Class that manages and provides toolchains and sysroots"""

import yaml
from os import walk, makedirs, getlogin
from abc import ABC
import general


# STATIC METHODS
class ToolchainManager(ABC):
    """"""

    __config_path: str
    __toolset: list

    @staticmethod
    def __parse_config_file() -> int:
        """Search ~/.amphimixis and parse in __toolset list"""

        makedirs(f"/home/{getlogin()}/.amphimixis", exist_ok=True)
        try:
            with open(f"/home/{getlogin()}/.amphimixis/toolset.yml", "r") as f:
                __toolset = yaml.safe_load(f)
                f.close()
        except:
            with open(f"/home/{getlogin()}/.amphimixis/toolset.yml", "w") as f:
                template = {
                    "platforms",
                    "compilers",
                    "sysroots",
                    "toolchains",
                }
                yaml.safe_dump(template, f)

        raise NotImplementedError

    @staticmethod
    def get_compiler_by_id(id: int) -> str:
        """"""

        raise NotImplementedError

    @staticmethod
    def get_sysroot_by_id(id: int) -> str:
        """"""

        raise NotImplementedError

    # HOW IDENTIFY MACHINE?
    @staticmethod
    def add_compiler(ip_machine: str, path: str, arch: general.Arch) -> None:
        """"""

        raise NotImplementedError

    @staticmethod
    def add_sysroot(ip_machine: str, path: str, arch: general.Arch) -> None:
        """"""

        raise NotImplementedError

    @staticmethod
    def install_to_sysroot(path_to_sysroot: str, *packages: str) -> int @ staticmethod:
        """"""

        raise NotImplementedError

    @staticmethod
    def remove_compiler(id: int) -> None:
        """"""

        raise NotImplementedError

    @staticmethod
    def remove_sysroot(id: int) -> None:
        """"""

        raise NotImplementedError
