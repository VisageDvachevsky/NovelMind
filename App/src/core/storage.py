import os
import json
from typing import Optional, Dict, List
from .encryption import AdvancedEncryptor
from LogSystem.LoggerSystem import Logger

logger = Logger(use_json=True)
log_class = logger.log_class()

@log_class
class SecureStorage:
    """
    A class to handle secure storage and retrieval of file metadata.
    """

    def __init__(self, base_path: str, master_password: str) -> None:
        """
        Initialize the SecureStorage with the base path and master password.

        :param base_path: The base directory path for storing file metadata.
        :param master_password: The master password for encryption and decryption.
        """
        self.base_path = base_path
        self.index_file = os.path.join(base_path, 'index.enc')
        self.encryptor = AdvancedEncryptor()
        self.master_password = master_password
        self.index = self._load_index()

    def _load_index(self) -> Dict[str, str]:
        """
        Load the file index from the encrypted index file.

        :return: The index as a dictionary.
        """
        if os.path.exists(self.index_file):
            with open(self.index_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.encryptor.decrypt(encrypted_data, self.master_password)
            return json.loads(decrypted_data)
        return {}

    def _save_index(self) -> None:
        """
        Save the current file index to the encrypted index file.
        """
        index_data = json.dumps(self.index).encode()
        encrypted_data = self.encryptor.encrypt(index_data, self.master_password)
        with open(self.index_file, 'wb') as f:
            f.write(encrypted_data)

    def add_file(self, file_id: str, encrypted_path: str) -> None:
        """
        Add a file to the index.

        :param file_id: The unique identifier for the file.
        :param encrypted_path: The path to the encrypted file.
        """
        self.index[file_id] = encrypted_path
        self._save_index()

    def get_file_path(self, file_id: str) -> Optional[str]:
        """
        Get the file path of a file by its file ID.

        :param file_id: The unique identifier for the file.
        :return: The path to the encrypted file.
        """
        return self.index.get(file_id)

    def remove_file(self, file_id: str) -> None:
        """
        Remove a file from the index.

        :param file_id: The unique identifier for the file.
        """
        if file_id in self.index:
            del self.index[file_id]
            self._save_index()

    def list_files(self) -> List[str]:
        """
        List all stored file IDs.

        :return: A list of file IDs.
        """
        return list(self.index.keys())
