from core.utils import is_valid_path
from core.file_handler import SecureFileHandler
from core.initializer import FileSystemInitializer
from typing import Optional

class SystemOperations:
    """
    A class to perform system operations such as deploying the file system.
    """

    @staticmethod
    def deploy(base_path: str, master_password: str) -> SecureFileHandler:
        """
        Deploy the file system by initializing it and returning a SecureFileHandler instance.

        :param base_path: The base directory path for storage initialization.
        :param master_password: The master password for encryption and decryption.
        :return: An instance of SecureFileHandler for managing secure file operations.
        :raises ValueError: If the base path is invalid.
        """
        if not is_valid_path(base_path):
            raise ValueError("Invalid base path")
        
        initializer = FileSystemInitializer(base_path, master_password)
        initializer.initialize()
        
        return SecureFileHandler(base_path, master_password)
