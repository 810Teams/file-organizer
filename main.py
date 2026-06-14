"""
    Main
"""


import os
import sys

from src.model.image_file import ImageFile
from src.utils import *
from settings import FOLDER_PATH_VALIDATOR, FILE_NAME_VALIDATOR, EXTENSION_VALIDATOR, RENAME_FUNCTION


def main() -> None:
    """ Main function """
    # Determine base folder name
    is_test: bool = '-test' in sys.argv
    base_path: str = str()

    print()
    if len(sys.argv) > 1 and sys.argv[1] != '-test':
        base_path = sys.argv[1]
        print('Base folder name is set to \'{}\'.'.format(base_path))

    # Rename
    file_list: list[ImageFile] = get_image_file_list(base_path, base_path=base_path)
    renamed_count: int = 0
    for f in file_list:
        if f.full_path != f.new_full_path:
            if not is_test:
                f.rename()
            print('  - Renamed `{}` to `{}`'.format(f.full_path, f.new_full_path))
            renamed_count += 1

    # Logging
    print()
    if renamed_count > 0:
        print('Total of {} file{} renamed.'.format(renamed_count, (renamed_count > 1) * 's'))
    else:
        print('No files renamed.')

    # Remove empty folders
    if not is_test:
        print()
        remove_empty_folder(base_path, base_path=base_path)


def get_image_file_list(current_directory: str, file_list: list[ImageFile]=list(), base_path: str=str()) -> list[ImageFile]:
    """ Returns a list containing all image files """
    directory_list: list[str] = os.listdir(current_directory if current_directory != str() else None)

    for directory in directory_list:
        try:
            # Recursive: Scan deeper directories
            get_image_file_list(path(current_directory if current_directory != str() else None, directory), file_list=file_list, base_path=base_path)
        except NotADirectoryError:
            image_file: ImageFile = ImageFile(
                path(current_directory, directory),
                base_path=base_path,
                folder_path_validator=FOLDER_PATH_VALIDATOR,
                file_name_validator=FILE_NAME_VALIDATOR,
                extension_validator=EXTENSION_VALIDATOR,
                rename_function=RENAME_FUNCTION
            )
            if image_file.validate():
                file_list.append(image_file)

    return file_list


def remove_empty_folder(current_directory: str, base_path: str=str()) -> None:
    """ Recursively removes all empty folders """
    try:
        directory_list: list[str] = os.listdir(current_directory if current_directory != str() else None)
    except NotADirectoryError:
        return

    for directory in directory_list:
        try:
            os.rmdir(path(current_directory if current_directory != str() else None, directory))
            print('  - Empty directory `{}` removed.'.format(path(current_directory if current_directory != str() else None, directory)))
        except OSError:
            remove_empty_folder(path(current_directory if current_directory != str() else None, directory), base_path=base_path)


main()
