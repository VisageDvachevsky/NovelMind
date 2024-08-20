import logging
from src.core.file_handler import SecureFileHandler

class FileOperations:
    def __init__(self, file_handler: SecureFileHandler) -> None:
        self.file_handler = file_handler
        self.current_directory = "root"
        self.logger = logging.getLogger(__name__)

    def _build_path(self, *parts):
        path = "/".join([self.current_directory] + list(parts))
        self.logger.debug(f"Built path: {path}")
        return path

    def add_file(self, file_path: str, file_id: str) -> None:
        dest_path = self._build_path(file_id)
        self.logger.info(f"Adding file from {file_path} to {dest_path}")
        self.file_handler.add_file(file_path, dest_path)

    def read_file(self, file_id: str, decode: bool = False) -> str:
        file_path = self._build_path(file_id)
        self.logger.info(f"Reading file {file_path} with decode={decode}")
        return self.file_handler.read_file(file_path, decode)

    def delete_file(self, file_id: str) -> None:
        file_path = self._build_path(file_id)
        self.logger.info(f"Deleting file {file_path}")
        self.file_handler.delete_file(file_path)

    def list_files(self) -> dict:
        self.logger.info("Listing files")
        return self.file_handler.list_files()

    def create_directory(self, dir_name: str) -> None:
        dir_path = self._build_path(dir_name)
        self.logger.info(f"Creating directory {dir_path}")
        self.file_handler.create_directory(dir_path)

    def rename_directory(self, old_name: str, new_name: str) -> None:
        old_path = self._build_path(old_name)
        new_path = self._build_path(new_name)
        self.logger.info(f"Renaming directory from {old_path} to {new_path}")
        self.file_handler.rename_directory(old_path, new_path)

    def delete_directory(self, dir_name: str) -> None:
        dir_path = self._build_path(dir_name)
        self.logger.info(f"Deleting directory {dir_path}")
        self.file_handler.delete_directory(dir_path)

    def move_file(self, file_id: str, dest_dir: str) -> None:
        src_path = self._build_path(file_id)
        dest_path = self._build_path(dest_dir, file_id)
        self.logger.info(f"Moving file from {src_path} to {dest_path}")
        self.file_handler.move_file(src_path, dest_path)

    def change_directory(self, dir_name: str) -> None:
        self.logger.info(f"Changing directory to {dir_name}")
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
        self.logger.info(f"Current directory: {self.current_directory}")
        return self.current_directory
