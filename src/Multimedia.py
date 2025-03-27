import os
import random
import re
import subprocess
import time

from src.constants import CHANGE_ALL_DATES_CMD, FILETYPE_CMD, FIX_METADATA_CMD


def _fix_time(hhmmss_str: str) -> str:
    """
    This function fixes possibly non-existent time string to an existing random time string.
    :param hhmmss_str: unfixed HHMMSS
    :type hhmmss_str: str
    :return: fixed HHMMSS
    :rtype: str
    """
    hhmmss_list: list[str] = re.findall(r"\d\d", hhmmss_str)

    if int(hhmmss_list[0]) < 0 or int(hhmmss_list[0]) > 23:
        hhmmss_list[0] = str(random.randint(10, 23))
    if int(hhmmss_list[1]) < 0 or int(hhmmss_list[1]) > 59:
        hhmmss_list[1] = str(random.randint(10, 59))
    if int(hhmmss_list[2]) < 0 or int(hhmmss_list[2]) > 59:
        hhmmss_list[2] = str(random.randint(10, 59))

    return "".join(hhmmss_list)


def _change_modify_date(file_path: str, date_str: str, hhmmss_str: str):
    """
    This function changes the modify date on a file.
    :param file_path:
    :type file_path: str
    :param date_str: YYYYMMDD
    :type date_str: str
    :param hhmmss_str: HHMMSS
    :type hhmmss_str: str
    """
    date_match = re.match(r"(\d{4})(\d\d)(\d\d)", date_str)
    hour_match = re.match(r"(\d\d)(\d\d)(\d\d)", hhmmss_str)

    if date_match and hour_match:
        year: int = int(date_match.group(1))
        month: int = int(date_match.group(2))
        day: int = int(date_match.group(3))

        hour: int = int(hour_match.group(1))
        minute: int = int(hour_match.group(2))
        second: int = int(hour_match.group(3))

        new_date: tuple[int, int, int, int, int, int] = (year, month, day, hour, minute, second)
        try:
            # 0 -> Day of the week. 0=Monday, but this parameter is ignored.
            # 0 -> Day of the year (1-366). It is calculated automatically if it is 0.
            # -1 -> Summer. 0=No, 1=Yes, -1=automatically detect.
            timestamp: float = time.mktime(new_date + (0, 0, -1))  # Convert to Unix timestamp
            os.utime(file_path, (timestamp, timestamp))  # (access_time, modify_time)
            print(f"{file_path} MODIFY DATE UPDATED")
        except Exception as e:
            print(f"Sorry, we cannot change the file name. {e}")


def _rename_file(old_path: str, new_path: str) -> str:
    """
    This function renames a file.
    :param old_path:
    :type old_path: str
    :param new_path:
    :type new_path: str
    :return: new_path
    :rtype: str
    """
    try:
        os.rename(old_path, new_path)
        print(f"RENAMED: {old_path} -> {new_path}")
        return new_path
    except Exception as e:
        print(f"Sorry, we cannot change the file name. {e}")


class Multimedia:
    def __init__(self, path: str):
        """
        This class works with images and videos. You can specify the root directory of your gallery
        as the 'path' parameter, because all its functions runs the path recursively.
        :param path:
        :type path: str
        """
        self._path: str = path
        self._filetype_cmd: str = FILETYPE_CMD.format(self._path)
        self._change_all_dates_cmd: str = CHANGE_ALL_DATES_CMD.format(self._path)
        self._fix_metadata_cmd: str = FIX_METADATA_CMD.format(self._path)

    @property
    def path(self) -> str:
        return self._path

    def _get_elements_list(self, path: str, elements_list: list[str], num_tabs: int) -> list[str]:
        """
        This recursive function runs through all the files and recursive directories to save it into 'elements_lists'.
        There are some rare parameters like 'num_tabs', but it is necessary to make the output prettier.
        :param path:
        :type path: str
        :param elements_list: The list that will be updated
        :type elements_list: list[str]
        :param num_tabs: Times an element of the list is tabbed
        :type num_tabs: int
        :return: elements_list updated
        :rtype: list[str]
        """
        tabs_str: str = ""
        for i in range(num_tabs):
            tabs_str += "\t"

        for element_name in os.listdir(path):
            element_path: str = os.path.join(path, element_name)
            if os.path.isfile(element_path):
                elements_list.append(f"{tabs_str}{element_name}")
            elif os.path.isdir(element_path):
                num_tabs += 1
                elements_list.append(f"{tabs_str}DIR: {element_name}")
                self._get_elements_list(element_path, elements_list, num_tabs)
            num_tabs -= 1
        return elements_list

    def print_elements_list(self):
        """
        It creates a list calling to the '_get_elements_list()' function and prints it.
        """
        elements_list: list[str] = []
        elements_list = self._get_elements_list(self._path, elements_list, 0)
        for element in elements_list:
            print(element)

    def rename_files(self, path: str):
        """
        This recursive function runs through all the files and recursive directories to rename the images and videos
        from IMG-YYYYMMDD-WA####.ext (or similar patterns) to the YYYYMMDD_######.ext format.
        :param path:
        :type path: str
        """
        for element_name in os.listdir(path):
            element_path: str = os.path.join(path, element_name)

            if os.path.isfile(element_path):
                # RegEx to find IMG-YYYYMMDD-WA####.ext pattern (or similar patterns)
                match = re.match(
                    r"(?:IMG|VID|Screenshot)[-_](\d{8})[-_](?:WA)?(\d{4,6})(?:[-_]\d{0,8}|\w+)?\.(\w+)",
                    element_name
                )
                if match:
                    date_str: str = match.group(1)
                    number_str: str = str(f"{int(match.group(2)):06d}")  # ':06d' fills the number with 0 until 6 digits
                    hhmmss_str: str = _fix_time(number_str)
                    extension_str: str = match.group(3)

                    # It renames the file in the expected format (YYYYMMDD_HHMMSS.ext)
                    new_name: str = f"{date_str}_{hhmmss_str}.{extension_str}"
                    new_path_name: str = os.path.join(path, new_name)
                    _rename_file(element_path, new_path_name)
                else:
                    print(f"{element_path} NOT RENAMED")
            elif os.path.isdir(element_path):
                self.rename_files(element_path)

    def change_all_modify_dates(self, path: str):
        """
        This recursive function runs through all the files and recursive directories to change all the modify dates.
        :param path:
        :type path: str
        """
        for element_name in os.listdir(path):
            element_path: str = os.path.join(path, element_name)

            if os.path.isfile(element_path):
                # RegEx to capture the date (YYYYMMDD) and the hour (HHMMSS)
                match = re.match(
                    r"(\d{8})[-_](\d{6}).*\.\w+",
                    element_name
                )
                if match:
                    date_str: str = match.group(1)
                    hhmmss_str: str = match.group(2)

                    _change_modify_date(element_path, date_str, hhmmss_str)
                else:
                    print(f"MODIFY DATE NOT CHANGED: {element_path}")
            elif os.path.isdir(element_path):
                self.change_all_modify_dates(element_path)

    def change_all_dates(self):
        """
        This function changes all file's date by writing
        'exiftool -r -fast -overwrite_original "-AllDates<FileModifyDate" "self._path"' in the cmd.
        """
        process: subprocess.Popen[bytes] = subprocess.Popen(
            self._change_all_dates_cmd,
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

    def fix_filetype(self):
        """
        This function creates an extensions list by taking the _get_filetype_list() recursive function.
        For each element from the list, it checks if the extension of the file is the real extension.
        If isn't the real extension, it changes to the real extension.
        """
        extensions_list: list[tuple[str, str, str]] = self.get_filetype_list()
        for element in extensions_list:
            old_ext: str = element[1]
            new_ext: str = element[2].lower()
            if old_ext == new_ext:
                print(f"{element[0]}.{old_ext} NOT RENAMED")
            else:
                _rename_file(
                    f"{element[0]}.{old_ext}",
                    f"{element[0]}.{new_ext}",
                )

    def get_filetype_list(self) -> list[tuple[str, str, str]]:
        """
        This function writes 'exiftool -r -fast -filetype "self._path"' in the cmd and captures the output
        to get this list: [(path, ext, real_ext), (path, ext, real_ext), ...]
        :return: [(path, ext, real_ext), (path, ext, real_ext), ...]
        :rtype: list[tuple[str, str, str]]:
        """
        process: subprocess.Popen[bytes] = subprocess.Popen(
            self._filetype_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        output, error = process.communicate()
        error_str: str = error.decode("utf-8")
        output_str: str = output.decode('utf-8').replace("\n", "")

        if error_str != "":
            print(error_str)

        extensions_list: list[tuple[str, str, str]] = re.findall(
            r"=+\s+([GC]:(?:[/\\]+[^.]+)?)\.(\w{2,5})\s+File Type\s+:\s+(\w{2,5})",
            output_str
        )
        return extensions_list
