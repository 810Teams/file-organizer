"""
    Settings
"""


import re

from typing import Callable

from src.utils import path


# Defined regular expressions
folder_path_regex: str = r'(.*)([0-9]{4}-[0-9]{2}-[0-9]{2})'
file_name_regex: str = r'([0-9]{4}-[0-9]{2}-[0-9]{2}_)?([0-9]{5}-[0-9]{6,16})(_[a-zA-Z0-9]+)?'
extension_regex: str = r'(.)(jpg|jpeg|png)'


# Path validation function: covers everything up until before the actual file (e.g. D:\GitHub\stable-diffusion-webui\outputs\txt2img-images\2026-06-12)
FOLDER_PATH_VALIDATOR: Callable[[str], bool] = lambda x: re.fullmatch(folder_path_regex, x)

# File name validation function: covers only the file name (extension excluded) (e.g. 00001-1234567890123345_extended)
FILE_NAME_VALIDATOR: Callable[[str], bool] = lambda x: re.fullmatch(file_name_regex, x)

# Extension validation function: covers only the extension (full stop included) (e.g. .png)
EXTENSION_VALIDATOR: Callable[[str], bool] = lambda x: re.fullmatch(extension_regex, x)

# File rename function
RENAME_FUNCTION = lambda base_path, folder_path, file_name, extension: path(
    re.fullmatch(r'(.*)([0-9]{4}-[0-9]{2}-[0-9]{2})', category)[1],
    '{}_{}{}{}'.format(
        re.fullmatch(folder_path_regex, folder_path)[2] if re.fullmatch(folder_path_regex, folder_path)[2] else '', # Memo: Put the date from the category into the file name
        re.fullmatch(file_name_regex, file_name)[2],                                                                # Memo: Remove the date from the file name if exists (re-ornagize)
        re.fullmatch(file_name_regex, file_name)[3] if re.fullmatch(file_name_regex, file_name)[3] else '',         # Memo: Keep any specifiers after the file name
        extension
    )
)
