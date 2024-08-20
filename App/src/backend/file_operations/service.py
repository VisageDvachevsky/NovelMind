from src.core.file_handler import SecureFileHandler
from typing import Dict
import os

class FileOperationsService:
    def __init__(self):
        self.file_handler = None
        self.current_directory = "root"

    def set_file_handler(self, file_handler: SecureFileHandler):
        self.file_handler = file_handler

    def _build_path(self, *parts):
        return "/".join([self.current_directory] + list(parts))

    def add_file(self, file_path: str, file_id: str):
        dest_path = self._build_path(file_id)
        self.file_handler.add_file(file_path, dest_path)

    def read_file(self, file_id: str, decode: bool = False) -> str:
        file_path = self._build_path(file_id)
        return self.file_handler.read_file(file_path, decode)

    def delete_file(self, file_id: str):
        file_path = self._build_path(file_id)
        self.file_handler.delete_file(file_path)

    def list_files(self) -> Dict:
        return self.file_handler.list_files()

    def create_directory(self, dir_name: str):
        dir_path = self._build_path(dir_name)
        self.file_handler.create_directory(dir_path)

    def rename_directory(self, old_name: str, new_name: str):
        old_path = self._build_path(old_name)
        new_path = self._build_path(new_name)
        self.file_handler.rename_directory(old_path, new_path)

    def delete_directory(self, dir_name: str):
        dir_path = self._build_path(dir_name)
        self.file_handler.delete_directory(dir_path)

    def move_file(self, file_id: str, dest_dir: str):
        src_path = self._build_path(file_id)
        dest_path = self._build_path(dest_dir, file_id)
        self.file_handler.move_file(src_path, dest_path)

    def change_directory(self, dir_name: str):
        if dir_name == "..":
            if self.current_directory != "root":
                self.current_directory = os.path.dirname(self.current_directory)
                if self.current_directory == "":
                    self.current_directory = "root"
        else:
            new_dir = self._build_path(dir_name)
            if self.file_handler.directory_exists(new_dir):
                self.current_directory = new_dir
            else:
                raise FileNotFoundError(f"Directory not found: {new_dir}")

    def get_current_directory(self) -> str:
        return self.current_directory