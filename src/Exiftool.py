import os
import re
import subprocess
import sys

from pathlib import Path

from src.constants import INSTALL_EXIFTOOL, ADD_EXIFTOOL_INTO_PATH, CHECK_EXIFTOOL


def _get_program_files():
    if sys.version_info >= (3, 6):  # Python 3.6 or newer installed
        return Path(os.environ["ProgramFiles"])
    else:
        return os.environ.get("ProgramFiles")


def _get_program_files_x86():
    if sys.version_info >= (3, 6):  # Python 3.6 or newer installed
        return Path(os.environ.get("ProgramFiles(x86)", ""))
    else:
        return os.environ.get("ProgramFiles(x86)")


class Exiftool:
    def __init__(self):
        self._program_files = _get_program_files()  # Default location for 64-bit programs
        self._program_files_x86 = _get_program_files_x86()  # For 32-bit programs on 64-bit Windows

        self._install_exiftool_cmd: str = INSTALL_EXIFTOOL
        # self._add_exiftool_into_path: str = ADD_EXIFTOOL_INTO_PATH
        self._add_exiftool_into_path_cmd: str = ADD_EXIFTOOL_INTO_PATH.format(f"%PATH%;{self._program_files}")
        self._check_exiftool_cmd: str = CHECK_EXIFTOOL
        # self._fix_metadata_cmd: str = FIX_METADATA_CMD.format(self._path_name)

        """
        print("Program Files:", program_files)
        print("Program Files (x86):", program_files_x86)
        """

    def check_exiftool(self):
        process: subprocess.Popen[bytes] = subprocess.Popen(
            self._check_exiftool_cmd,
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
