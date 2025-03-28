import distro
import os
import platform
import subprocess
import sys

from pathlib import Path

from src.constants import (
    CHECK_EXIFTOOL_CMD,
    INSTALL_EXIFTOOL_WIN,
    INSTALL_EXIFTOOL_LINUX,
    INSTALL_EXIFTOOL_MACOS,
    ADD_EXIFTOOL_ON_PATH
)


def _get_program_files():  # windows
    """
    This function returns 'Program Files' dir.
    :return: Program Files
    :rtype: Path | str | None
    """
    if sys.version_info >= (3, 6):  # Python 3.6 or newer installed
        return Path(os.environ["ProgramFiles"])
    else:
        return os.environ.get("ProgramFiles")


def _get_program_files_x86():  # windows
    """
    This function returns 'Program Files x86' dir.
    :return: Program Files x86
    :rtype: Path | str | None
    """
    if sys.version_info >= (3, 6):  # Python 3.6 or newer installed
        return Path(os.environ.get("ProgramFiles(x86)", ""))
    else:
        return os.environ.get("ProgramFiles(x86)")


def _install_exiftool_cmd(install_exiftool_cmd: str):
    """
    This function installs exiftool on the cmd.
    :param install_exiftool_cmd:
    :type install_exiftool_cmd: str
    """
    process: subprocess.Popen[bytes] = subprocess.Popen(
        install_exiftool_cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = process.communicate()
    error_str: str = error.decode("utf-8")
    output_str: str = output.decode("utf-8")

    if error_str != "":
        print(error_str)
    print(output_str)


def _check_exiftool() -> str | None:
    """
    This function checks if exiftool is installed.
    :return: Exiftool version
    :rtype: str | None
    """
    process: subprocess.Popen[bytes] = subprocess.Popen(
        CHECK_EXIFTOOL_CMD,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = process.communicate()
    error_str: str = error.decode("utf-8")
    output_str: str = output.decode("utf-8")

    if error_str != "":
        print(error_str)
    return output_str


class Exiftool:
    def __init__(self):
        self._program_files = _get_program_files()  # Default location for 64-bit programs
        self._program_files_x86 = _get_program_files_x86()  # For 32-bit programs on 64-bit Windows

        self._add_exiftool_on_path_cmd: str = ADD_EXIFTOOL_ON_PATH.format(f"%PATH%;{self._program_files}")

    def _add_exiftool_on_path(self):
        """
        This function adds the program into a path to run on the cmd.
        """
        process: subprocess.Popen[bytes] = subprocess.Popen(
            self._add_exiftool_on_path_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        error_str: str = error.decode("utf-8")
        output_str: str = output.decode("utf-8")

        if error_str != "":
            print(error_str)
        print(output_str)

    def install_exiftool(self):
        """
        This function calls the _add_exiftool_on_path() function
        to install exiftool with different commands depending on the OS.
        """
        exiftool_v: str | None = _check_exiftool()
        if exiftool_v == "" or exiftool_v is None:
            print("Installing exiftool...")
            os_name: str = platform.system().lower()
            if os_name == "windows":
                _install_exiftool_cmd(INSTALL_EXIFTOOL_WIN)
                self._add_exiftool_on_path()
            elif os_name == "linux":
                linux_distro: str = distro.id().lower() or "unknown"
                if "ubuntu" in linux_distro or "debian" in linux_distro:
                    _install_exiftool_cmd(INSTALL_EXIFTOOL_LINUX["ubuntu/debian"])
                elif "arch" in linux_distro:
                    _install_exiftool_cmd(INSTALL_EXIFTOOL_LINUX["arch"])
                elif "fedora" in linux_distro:
                    _install_exiftool_cmd(INSTALL_EXIFTOOL_LINUX["fedora"])
                elif "suse" in linux_distro:
                    _install_exiftool_cmd(INSTALL_EXIFTOOL_LINUX["suse"])
                else:
                    _install_exiftool_cmd(INSTALL_EXIFTOOL_LINUX["unknown"])
                self._add_exiftool_on_path()
            elif os_name == "darwin":
                _install_exiftool_cmd(INSTALL_EXIFTOOL_MACOS)
                self._add_exiftool_on_path()
            else:
                raise Exception("Unsupported OS")
        else:
            print("Exiftool is already downloaded.")
