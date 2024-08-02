import os

def create_directory_if_not_exists(path: str) -> None:
    """
    Create a directory if it does not already exist.

    :param path: The path of the directory to create.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def is_valid_path(path: str) -> bool:
    """
    Check if a path is a valid directory path.

    :param path: The path to check.
    :return: True if the path is valid and is a directory, False otherwise.
    """
    return os.path.exists(path) and os.path.isdir(path)
