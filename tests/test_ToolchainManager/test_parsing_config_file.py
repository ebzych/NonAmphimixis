from os import remove, getlogin, path
from shutil import rmtree
import yaml


# pylint: disable=relative-beyond-top-level
from src.general import ToolchainManager  # type: ignore


class FriendToolchainManager(ToolchainManager):
    """Class then break encupsulation of ToolchainManager for testing him"""

    @staticmethod
    def public_parse_config_file():
        """Public ToolchainManager._parse_config_file()"""
        ToolchainManager._parse_config_file()


def is_file_exists_and_correct(pth: str) -> bool:
    """Check if file creating correct"""
    is_exists = path.exists(pth)

    is_correct_filled = False
    with open(
        f"/home/{getlogin()}/.config/amphimixis/toolset.yml", "r", encoding="utf-8"
    ) as f:
        toolset = yaml.safe_load(f)
        is_correct_filled = toolset.keys() == {"compilers", "platforms", "sysroots"}
    return is_exists and is_correct_filled


def test_creating_dir() -> None:
    """
    Remove f"/home/{getlogin}/.config/amphimixis" and call _parse_config_file()
    Expected: create directory f"/home/{getlogin}/.config/amphimixis"
    """
    if path.exists(f"/home/{getlogin()}/.config/amphimixis"):
        rmtree(f"/home/{getlogin()}/.config/amphimixis")

    FriendToolchainManager.public_parse_config_file()
    assert path.exists(f"/home/{getlogin()}/.config/amphimixis")


def test_creating_file() -> None:
    """
    Remove f"/home/{getlogin}/.config/amphimixis/toolset.yml" and call _parse_config_file()
    Expected: create file f"/home/{getlogin}/.config/amphimixis/toolset.yml" and fill it correct
    """
    if path.exists(f"/home/{getlogin()}/.config/amphimixis/toolset.yml"):
        remove(f"/home/{getlogin()}/.config/amphimixis/toolset.yml")

    FriendToolchainManager.public_parse_config_file()
    assert is_file_exists_and_correct(
        f"/home/{getlogin()}/.config/amphimixis/toolset.yml"
    )


def test_creating_dir_and_file():
    """Test if directory and file creating correct"""
    rmtree(f"/home/{getlogin()}/.config/amphimixis")
    FriendToolchainManager.public_parse_config_file()

    assert path.exists(f"/home/{getlogin()}/.config/amphimixis")
    assert is_file_exists_and_correct(
        f"/home/{getlogin()}/.config/amphimixis/toolset.yml"
    )
