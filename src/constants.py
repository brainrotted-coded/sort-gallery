# Exiftool.py CMD
CHECK_EXIFTOOL_CMD: str = 'exiftool -ver'
INSTALL_EXIFTOOL_WIN: str = 'winget install PhilHarvey.ExifTool'
INSTALL_EXIFTOOL_LINUX: dict[str, str] = {
    'ubuntu/debian': 'sudo apt install libimage-exiftool-perl',
    'arch': 'sudo pacman -S perl-image-exiftool',
    'fedora': 'sudo dnf install perl-Image-ExifTool',
    'suse': 'sudo zypper install exiftool',
    'unknown': 'wget https://exiftool.org/Image-ExifTool.tar.gz && tar -xzf Image-ExifTool.tar.gz && cd Image-ExifTool-* && perl Makefile.PL && make test && sudo make install'
}
INSTALL_EXIFTOOL_MACOS: str = 'brew install exiftool'
ADD_EXIFTOOL_ON_PATH: str = 'setx PATH "{}"'

# Multimedia.py CMD
CHANGE_ALL_DATES_CMD: str = 'exiftool -r -fast -overwrite_original "-AllDates<FileModifyDate" "{}"'
FILETYPE_CMD: str = 'exiftool -r -fast -filetype "{}"'
FIX_METADATA_CMD: str = 'exiftool -r -fast -overwrite_original "{}"'
