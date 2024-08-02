from typing import Optional, List, Dict
from src.core.encryption import EncryptionManager
from src.core.file_manager import FileManager
from src.core.identifier import IdentifierManager
from src.core.storage import StorageManager
from src.core.key_management import KeyManager
from src.core.integrity import IntegrityManager

import logging
logging.basicConfig(level=logging.INFO)

class FileInterface:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.identifier_manager = IdentifierManager()
        self.integrity_manager = IntegrityManager()

    def _initialize_managers(self, data_key: bytes, metadata_key: bytes):
        self.encryption_manager = EncryptionManager(data_key)
        self.storage_manager = StorageManager(self.storage_path, metadata_key)
        self.file_manager = FileManager(self.encryption_manager, self.identifier_manager, self.storage_manager)

    def upload_file(self, file_path: str, data_key: bytes, metadata_key: bytes) -> str:
        self._initialize_managers(data_key, metadata_key)
        file_id = self.file_manager.add_file(file_path)
        if file_id:
            logging.info(f"File {file_path} uploaded with file ID {file_id}.")
        else:
            logging.error(f"Failed to upload file {file_path}.")
        return file_id

    def download_file(self, file_id: str, data_key: bytes, metadata_key: bytes) -> Optional[bytes]:
        self._initialize_managers(data_key, metadata_key)
        return self.file_manager.retrieve_file(file_id)

    def delete_file(self, file_id: str, data_key: bytes, metadata_key: bytes) -> None:
        self._initialize_managers(data_key, metadata_key)
        self.file_manager.delete_file(file_id)
        logging.info(f"File with ID {file_id} deleted.")

    def check_file_integrity(self, file_id: str, data_key: bytes, metadata_key: bytes) -> bool:
        self._initialize_managers(data_key, metadata_key)
        data = self.file_manager.retrieve_file(file_id)
        if data:
            metadata = self.storage_manager.get_file_metadata(file_id)
            return self.integrity_manager.verify_data(data, metadata['hash'])
        logging.error(f"Failed to retrieve file {file_id} for integrity check.")
        return False

    def list_files(self, data_key: bytes, metadata_key: bytes) -> List[str]:
        self._initialize_managers(data_key, metadata_key)
        return list(self.storage_manager.metadata.keys())

    def get_file_info(self, file_id: str, data_key: bytes, metadata_key: bytes) -> Optional[Dict]:
        self._initialize_managers(data_key, metadata_key)
        metadata = self.storage_manager.get_file_metadata(file_id)
        logging.info(f"Retrieved metadata for file ID {file_id}: {metadata}")
        return metadata if metadata else None