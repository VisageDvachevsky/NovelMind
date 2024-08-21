from core.utils import is_valid_path
from core.file_handler import SecureFileHandler
from core.initializer import FileSystemInitializer

class SystemOperations:
    @staticmethod
    def deploy(base_path: str, master_password: str) -> SecureFileHandler:
        if not is_valid_path(base_path):
            raise ValueError("Invalid base path")

        initializer = FileSystemInitializer(base_path, master_password)
        initializer.initialize()

        return SecureFileHandler(base_path, master_password)