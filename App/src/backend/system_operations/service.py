from src.core.utils import is_valid_path
from src.core.file_handler import SecureFileHandler
from src.core.initializer import FileSystemInitializer

class SystemOperationsService:
    @staticmethod
    def deploy(base_path: str, master_password: str) -> None:
        if not is_valid_path(base_path):
            raise ValueError("Invalid base path")
        initializer = FileSystemInitializer(base_path, master_password)
        initializer.initialize()