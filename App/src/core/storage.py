import os
import json
from typing import Optional
from src.core.encryption import EncryptionManager

class StorageManager:
    def __init__(self, storage_path: str, metadata_key: bytes):
        self.storage_path = storage_path
        self.metadata_file = os.path.join(self.storage_path, 'metadata.json')
        self.metadata_key = metadata_key
        self.encryption_manager = EncryptionManager(metadata_key)
        self.metadata = self._load_metadata()

        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def _load_metadata(self) -> dict:
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'rb') as file:
                encrypted_metadata = file.read()
                decrypted_metadata = self.encryption_manager.decrypt(encrypted_metadata)
                return json.loads(decrypted_metadata.decode())
        return {}

    def _save_metadata(self) -> None:
        encrypted_metadata = self.encryption_manager.encrypt(json.dumps(self.metadata).encode())
        with open(self.metadata_file, 'wb') as file:
            file.write(encrypted_metadata)

    def save_file(self, file_id: str, data: bytes, original_path: str, hash_value: str) -> None:
        file_path = os.path.join(self.storage_path, file_id)
        with open(file_path, 'wb') as file:
            file.write(data)

        self.metadata[file_id] = {'original_path': original_path, 'hash': hash_value}
        self._save_metadata()

    def load_file(self, file_id: str) -> Optional[bytes]:
        file_path = os.path.join(self.storage_path, file_id)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                return file.read()
        return None

    def delete_file(self, file_id: str) -> None:
        file_path = os.path.join(self.storage_path, file_id)
        if os.path.exists(file_path):
            os.remove(file_path)
            del self.metadata[file_id]
            self._save_metadata()

    def get_file_metadata(self, file_id: str) -> Optional[dict]:
        return self.metadata.get(file_id)