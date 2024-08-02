import os
import json
import logging
from typing import Optional
from src.core.encryption import EncryptionManager

logging.basicConfig(level=logging.INFO)

class StorageManager:
    def __init__(self, storage_path: str, metadata_key: bytes):
        self.storage_path = storage_path
        self.metadata_file = os.path.join(self.storage_path, 'metadata.json')
        self.metadata_key = metadata_key
        self.encryption_manager = EncryptionManager(metadata_key)
        self.metadata = self._load_metadata()

        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            logging.info(f"Storage path {self.storage_path} created.")

    def _load_metadata(self) -> dict:
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'rb') as file:
                    encrypted_metadata = file.read()
                    decrypted_metadata = self.encryption_manager.decrypt(encrypted_metadata)
                    logging.info("Metadata loaded successfully.")
                    return json.loads(decrypted_metadata.decode())
            except Exception as e:
                logging.error(f"Failed to load metadata: {e}")
                return {}
        return {}

    def _save_metadata(self) -> None:
        try:
            encrypted_metadata = self.encryption_manager.encrypt(json.dumps(self.metadata).encode())
            with open(self.metadata_file, 'wb') as file:
                file.write(encrypted_metadata)
            logging.info("Metadata saved successfully.")
        except Exception as e:
            logging.error(f"Failed to save metadata: {e}")

    def save_file(self, file_id: str, data: bytes, original_path: str, hash_value: str) -> None:
        try:
            file_path = os.path.join(self.storage_path, file_id)
            with open(file_path, 'wb') as file:
                file.write(data)
                logging.info(f"File {file_id} saved to {file_path}.")

            self.metadata[file_id] = {'original_path': original_path, 'hash': hash_value}
            self._save_metadata()
        except Exception as e:
            logging.error(f"Failed to save file {file_id}: {e}")

    def load_file(self, file_id: str) -> Optional[bytes]:
        file_path = os.path.join(self.storage_path, file_id)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as file:
                    logging.info(f"File {file_id} loaded from {file_path}.")
                    return file.read()
            except Exception as e:
                logging.error(f"Failed to load file {file_id}: {e}")
        logging.warning(f"File {file_id} does not exist in storage.")
        return None

    def delete_file(self, file_id: str) -> None:
        file_path = os.path.join(self.storage_path, file_id)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logging.info(f"File {file_id} deleted from {file_path}.")
                if file_id in self.metadata:
                    del self.metadata[file_id]
                    self._save_metadata()
            except Exception as e:
                logging.error(f"Failed to delete file {file_id}: {e}")

    def get_file_metadata(self, file_id: str) -> Optional[dict]:
        return self.metadata.get(file_id)