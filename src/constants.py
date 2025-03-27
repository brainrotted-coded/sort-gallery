# Multimedia.py CMD
CHANGE_ALL_DATES_CMD: str = 'exiftool -r -fast -overwrite_original "-AllDates<FileModifyDate" "{}"'
FILETYPE_CMD: str = 'exiftool -r -fast -filetype "{}"'
FIX_METADATA_CMD: str = 'exiftool -r -fast -overwrite_original "{}"'
