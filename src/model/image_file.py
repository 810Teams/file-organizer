"""
    Image file model
"""


import os

from typing import Callable

from src.utils import path


class ImageFile:
    """ Image file class """
    def __init__(
        self,
        full_path: str,
        rename_function: Callable[[str, str, str, str], str],
        base_path: str='',
        path_validator: Callable[[str], bool]=lambda x: True,
        file_name_validator: Callable[[str], bool]=lambda x: True,
        extension_validator: Callable[[str], bool]=lambda x: True
    ):
        self.full_path: str = full_path
        self.rename_pattern: Callable[[str, str, str, str], str] = rename_function
        self.base_path: str = base_path
        self.path_validator: Callable[[str], bool] = path_validator
        self.file_name_validator: Callable[[str], bool] = file_name_validator
        self.extension_validator: Callable[[str], bool] = extension_validator

    @property
    def category_path(self) -> str:
        return path(*self.full_path.replace(self.base_path, str(), 1).split('/')[:-1])

    @property
    def file_name(self) -> str:
        return self.full_path.split('/')[-1].split('.')[0]

    @property
    def extension(self) -> str:
        split_file_name = self.full_path.rsplit('.', 1)
        if len(split_file_name) <= 1:
            return None

        extension = split_file_name[-1]
        if extension.isdigit():
            return None

        return '.{}'.format(extension)

    @property
    def new_full_path(self) -> str:
        return path(self.rename_pattern(self.base_path, self.category_path, self.file_name, self.extension))

    def validate(self) -> bool:
        return self.path_validator(self.category_path) and self.file_name_validator(self.file_name) and self.extension_validator(self.extension)

    def rename(self) -> None:
        if self.full_path != self.new_full_path:
            try:
                os.rename(self.full_path.lstrip('/'), self.new_full_path.lstrip('/'))
            except FileNotFoundError:
                os.makedirs(path(*self.new_full_path.lstrip('/').split('/')[:-1]))
                self.rename()
            except FileExistsError:
                pass
