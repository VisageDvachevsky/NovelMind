from src.core.file_encryption import FileEncryption
from src.core.storage_handler import StorageHandler
import os

class FileManager:
    def __init__(self, base_directory: str, encryption_key: bytes):
        self.storage_handler = StorageHandler(base_directory)
        self.file_encryption = FileEncryption(encryption_key)

    def add_file(self, file_path: str, file_id: str) -> None:
        """Encrypts and stores a file."""
        encrypted_data = self.file_encryption.encrypt_file(file_path)
        self.storage_handler.store_data(file_id, encrypted_data)

    def get_file_data(self, file_id: str) -> bytes:
        """Retrieves and decrypts file data by its ID."""
        encrypted_data = self.storage_handler.retrieve_data(file_id)
        decrypted_data = self.file_encryption.decrypt_file(encrypted_data)
        return decrypted_data

    def delete_file(self, file_id: str) -> None:
        """Deletes a file from the storage."""
        self.storage_handler.delete_data(file_id)

    def list_files(self) -> dict:
        """Lists all files with their IDs."""
        files = {}
        for file_name in os.listdir(self.storage_handler.base_directory):
            if file_name.endswith('.enc'):
                file_id = file_name[:-4] 
                files[file_id] = self.get_file_data(file_id)
        return files