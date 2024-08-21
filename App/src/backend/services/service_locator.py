import logging
from .system_operations_service import SystemOperationsService
from .file_operations_service import FileOperationsService

logger = logging.getLogger(__name__)

class ServiceLocator:
    __system_service : SystemOperationsService = None
    __file_service : FileOperationsService = None
    
    @staticmethod
    def get_system_service() -> SystemOperationsService:
        if not ServiceLocator.__system_service:
            ServiceLocator.__system_service = SystemOperationsService()
        
        return ServiceLocator.__system_service
    
    @staticmethod
    def get_file_service() -> FileOperationsService:
        if ServiceLocator.__file_service == None:
            systemService = ServiceLocator.get_system_service()
            file_handler = systemService.file_handler
            
            if not file_handler:
                logger.error("Can't initialize FileOperationsService before file system was deployed.")
                raise RuntimeError("File handler of SystemOperationsService was None.")
            
            ServiceLocator.__file_service = FileOperationsService(file_handler)
            
        return ServiceLocator.__file_service
                
            
            