from typing import Optional
from src.core.encryption import EncryptionManager
from src.core.identifier import IdentifierManager
from src.core.storage import StorageManager

class FileManager:
    def __init__(self, encryption_manager: EncryptionManager, identifier_manager: IdentifierManager, storage_manager: StorageManager):
        self.encryption_manager = encryption_manager
        self.identifier_manager = identifier_manager
        self.storage_manager = storage_manager

    def add_file(self, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            data = file.read()

        file_id = self.identifier_manager.generate_identifier()
        encrypted_data = self.encryption_manager.encrypt(data)
        hash_value = self.encryption_manager.hash_data(data)

        self.storage_manager.save_file(file_id, encrypted_data, file_path, hash_value)

        return file_id

    def retrieve_file(self, file_id: str) -> Optional[bytes]:
        encrypted_data = self.storage_manager.load_file(file_id)
        metadata = self.storage_manager.get_file_metadata(file_id)

        if encrypted_data and metadata:
            decrypted_data = self.encryption_manager.decrypt(encrypted_data)
            if self.encryption_manager.hash_data(decrypted_data) == metadata['hash']:
                return decrypted_data

        return None

    def delete_file(self, file_id: str) -> None:
        self.storage_manager.delete_file(file_id)