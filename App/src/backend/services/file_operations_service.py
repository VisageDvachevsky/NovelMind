import logging
from src.core.file_handler import SecureFileHandler
from typing import Dict
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class FileOperationsService:
    def __init__(self, fileHandler : SecureFileHandler):
        self.fileHandler = fileHandler
        self.current_directory = "root"
        logger.debug(f"Initialized FileOperationsService with current_directory: {self.current_directory}")

    def set_file_handler(self, fileHandler: SecureFileHandler):
        self.fileHandler = fileHandler
        logger.debug(f"File handler set: {fileHandler}")

    def _build_path(self, *parts):
        path = "/".join([self.current_directory] + list(parts))
        logger.debug(f"Built path: {path}")
        return path

    def add_file(self, file_path: str, file_id: str):
        dest_path = self._build_path(file_id)
        logger.debug(f"Adding file from {file_path} to {dest_path}")
        self.fileHandler.add_file(file_path, dest_path)
        logger.info(f"File added successfully from {file_path} to {dest_path}")

    def read_file(self, file_id: str, decode: bool = False) -> str:
        file_path = self._build_path(file_id)
        logger.debug(f"Reading file at {file_path} with decode={decode}")
        content = self.fileHandler.read_file(file_path, decode)
        logger.info(f"File read successfully at {file_path}")
        return content

    def delete_file(self, file_id: str):
        file_path = self._build_path(file_id)
        logger.debug(f"Deleting file at {file_path}")
        self.fileHandler.delete_file(file_path)
        logger.info(f"File deleted successfully at {file_path}")

    def list_files(self) -> Dict:
        logger.debug(f"Listing files in current directory: {self.current_directory}")
        files = self.fileHandler.list_files()
        logger.info(f"Files listed successfully in directory: {self.current_directory}")
        return files

    def create_directory(self, dir_name: str):
        dir_path = self._build_path(dir_name)
        logger.debug(f"Creating directory at {dir_path}")
        self.fileHandler.create_directory(dir_path)
        logger.info(f"Directory created successfully at {dir_path}")

    def rename_directory(self, old_name: str, new_name: str):
        old_path = self._build_path(old_name)
        new_path = self._build_path(new_name)
        logger.debug(f"Renaming directory from {old_path} to {new_path}")
        self.fileHandler.rename_directory(old_path, new_path)
        logger.info(f"Directory renamed successfully from {old_path} to {new_path}")

    def delete_directory(self, dir_name: str):
        dir_path = self._build_path(dir_name)
        logger.debug(f"Deleting directory at {dir_path}")
        self.fileHandler.delete_directory(dir_path)
        logger.info(f"Directory deleted successfully at {dir_path}")

    def move_file(self, file_id: str, dest_dir: str):
        src_path = self._build_path(file_id)
        dest_path = self._build_path(dest_dir, file_id)
        logger.debug(f"Moving file from {src_path} to {dest_path}")
        self.fileHandler.move_file(src_path, dest_path)
        logger.info(f"File moved successfully from {src_path} to {dest_path}")

    def change_directory(self, dir_name: str):
        logger.debug(f"Changing directory to {dir_name}")
        if dir_name == "..":
            if self.current_directory != "root":
                previous_directory = self.current_directory
                self.current_directory = os.path.dirname(self.current_directory)
                if self.current_directory == "":
                    self.current_directory = "root"
                logger.debug(f"Changed directory from {previous_directory} to {self.current_directory}")
        else:
            new_dir = self._build_path(dir_name)
            if self.fileHandler.directory_exists(new_dir):
                self.current_directory = new_dir
                logger.debug(f"Changed directory to {new_dir}")
            else:
                error_msg = f"Directory not found: {new_dir}"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)

    def get_current_directory(self) -> str:
        logger.debug(f"Getting current directory: {self.current_directory}")
        return self.current_directory
