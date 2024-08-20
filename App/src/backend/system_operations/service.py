import logging
from core.utils import is_valid_path
from core.file_handler import SecureFileHandler
from core.initializer import FileSystemInitializer

class SystemOperations:
    @staticmethod
    def deploy(base_path: str, master_password: str) -> SecureFileHandler:
        logger = logging.getLogger(__name__)
        logger.info(f"Deploying file system at base path: {base_path}")

        if not is_valid_path(base_path):
            logger.error(f"Invalid base path: {base_path}")
            raise ValueError("Invalid base path")

        initializer = FileSystemInitializer(base_path, master_password)
        initializer.initialize()

        logger.info("File system initialized successfully")
        return SecureFileHandler(base_path, master_password)
