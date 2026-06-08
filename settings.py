"""
    Settings
"""


import re

from typing import Callable

from src.utils import path


PATH_VALIDATOR: Callable[[str], bool] = lambda x: re.fullmatch(r'(.*)([0-9]{4}-[0-9]{2}-[0-9]{2})', x)
FILE_NAME_VALIDATOR: Callable[[str], bool] = lambda x: re.fullmatch(r'([0-9]{5}-[0-9]{6,16})(_[a-zA-Z0-9]+)?', x)
EXTENSION_VALIDATOR: Callable[[str], bool] = lambda x: re.fullmatch(r'(.)(jpg|jpeg|png)', x)

RENAME_FUNCTION = lambda base, category, file_name, extension: path(
    base,
    re.fullmatch(r'(.*)([0-9]{4}-[0-9]{2}-[0-9]{2})', category)[1],
    '{}_{}{}'.format(
        re.fullmatch(r'(.*)([0-9]{4}-[0-9]{2}-[0-9]{2})', category)[2],
        file_name,
        extension
    )
)
