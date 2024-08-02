import os

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def is_valid_path(path):
    return os.path.exists(path) and os.path.isdir(path)