import os

def create_directory_if_not_exists(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def is_valid_path(path: str) -> bool:
    if not path:
        return False
    return os.path.exists(path) and os.path.isdir(path)
