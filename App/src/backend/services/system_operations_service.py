from src.core.utils import is_valid_path
from src.core.initializer import FileSystemInitializer
from src.core.file_handler import SecureFileHandler

class SystemOperationsService:
    def __init__(self) -> None:
        self.__fileHandler : SecureFileHandler = None
    
    @property
    def file_handler(self) -> SecureFileHandler:
        return self.__fileHandler
    
    def deploy(self, base_path: str, master_password: str) -> None:
        if not is_valid_path(base_path):
            raise ValueError("Invalid base path")
        initializer = FileSystemInitializer(base_path, master_password)
        initializer.initialize()
        
        self.__fileHandler = SecureFileHandler(base_path, master_password)