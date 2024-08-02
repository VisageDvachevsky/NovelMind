from typing import Optional, List
from src.core.encryption import EncryptionManager
from src.core.file_manager import FileManager
from src.core.identifier import IdentifierManager
from src.core.storage import StorageManager
from src.core.access_control import AccessControlManager
from src.core.key_management import KeyManager
from src.core.integrity import IntegrityManager

class FileInterface:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.identifier_manager = IdentifierManager()
        self.access_control_manager = AccessControlManager()
        self.integrity_manager = IntegrityManager()

    def _initialize_managers(self, data_key: bytes, metadata_key: bytes):
        self.encryption_manager = EncryptionManager(data_key)
        self.storage_manager = StorageManager(self.storage_path, metadata_key)
        self.file_manager = FileManager(self.encryption_manager, self.identifier_manager, self.storage_manager)

    def upload_file(self, file_path: str, user_id: str, data_key: bytes, metadata_key: bytes) -> str:
        self._initialize_managers(data_key, metadata_key)
        file_id = self.file_manager.add_file(file_path)
        self.access_control_manager.set_permissions(file_id, user_id, 'read')
        return file_id

    def download_file(self, file_id: str, user_id: str, data_key: bytes, metadata_key: bytes) -> Optional[bytes]:
        self._initialize_managers(data_key, metadata_key)
        if self.access_control_manager.check_permission(file_id, user_id, 'read'):
            return self.file_manager.retrieve_file(file_id)
        raise PermissionError("Access Denied")

    def delete_file(self, file_id: str, user_id: str, data_key: bytes, metadata_key: bytes) -> None:
        self._initialize_managers(data_key, metadata_key)
        if self.access_control_manager.check_permission(file_id, user_id, 'delete'):
            self.file_manager.delete_file(file_id)
        else:
            raise PermissionError("Access Denied")

    def set_file_permissions(self, file_id: str, user_id: str, permission_type: str, data_key: bytes, metadata_key: bytes) -> None:
        self._initialize_managers(data_key, metadata_key)
        self.access_control_manager.set_permissions(file_id, user_id, permission_type)

    def check_file_integrity(self, file_id: str, user_id: str, data_key: bytes, metadata_key: bytes) -> bool:
        self._initialize_managers(data_key, metadata_key)
        if self.access_control_manager.check_permission(file_id, user_id, 'read'):
            data = self.file_manager.retrieve_file(file_id)
            if data:
                metadata = self.storage_manager.get_file_metadata(file_id)
                return self.integrity_manager.verify_data(data, metadata['hash'])
        raise PermissionError("Access Denied")

    def list_files(self, user_id: str, data_key: bytes, metadata_key: bytes) -> List[str]:
        self._initialize_managers(data_key, metadata_key)
        accessible_files = []
        for file_id in self.storage_manager.metadata.keys():
            if self.access_control_manager.check_permission(file_id, user_id, 'read'):
                accessible_files.append(file_id)
        return accessible_files
