import os
import base64
from typing import Optional, List
from .encryption import AdvancedEncryptor
from .storage import SecureStorage
from LogSystem.LoggerSystem import Logger

logger = Logger(use_json=True)
log_class = logger.log_class()

@log_class
class SecureFileHandler:
    """
    A class to handle secure file operations such as adding, reading, deleting, and listing files.
    """

    def __init__(self, base_path: str, master_password: str) -> None:
        """
        Initialize the SecureFileHandler with the base path and master password.

        :param base_path: The base directory path for storing files.
        :param master_password: The master password for encryption and decryption.
        """
        self.base_path = base_path
        self.encryptor = AdvancedEncryptor()
        self.storage = SecureStorage(base_path, master_password)
        self.master_password = master_password

    def add_file(self, file_path: str, file_id: str) -> None:
        """
        Add and encrypt a file with a given file ID.

        :param file_path: The path to the file to be added.
        :param file_id: The unique identifier for the file.
        """
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        encrypted_content = self.encryptor.encrypt(file_content, self.master_password)
        encrypted_file_path = os.path.join(self.base_path, f'{file_id}.enc')
        
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_content)
        
        self.storage.add_file(file_id, encrypted_file_path)

    def read_file(self, file_id: str, decode: bool = False) -> str:
        """
        Read and decrypt a file by its file ID.

        :param file_id: The unique identifier for the file.
        :param decode: Whether to decode the decrypted content as UTF-8 string or base64.
        :return: The decrypted content as a string.
        :raises FileNotFoundError: If the file with the specified ID is not found.
        """
        encrypted_file_path = self.storage.get_file_path(file_id)
        if not encrypted_file_path:
            raise FileNotFoundError(f"File with id {file_id} not found")

        with open(encrypted_file_path, 'rb') as f:
            encrypted_content = f.read()
        
        decrypted_content = self.encryptor.decrypt(encrypted_content, self.master_password)
        
        if decode:
            try:
                return decrypted_content.decode('utf-8')
            except UnicodeDecodeError:
                return base64.b64encode(decrypted_content).decode('utf-8')
        else:
            return decrypted_content

    def delete_file(self, file_id: str) -> None:
        """
        Delete a file by its file ID.

        :param file_id: The unique identifier for the file.
        :raises FileNotFoundError: If the file with the specified ID is not found.
        """
        encrypted_file_path = self.storage.get_file_path(file_id)
        if not encrypted_file_path:
            raise FileNotFoundError(f"File with id {file_id} not found")

        os.remove(encrypted_file_path)
        self.storage.remove_file(file_id)

    def list_files(self) -> List[str]:
        """
        List all stored file IDs.

        :return: A list of file IDs.
        """
        return self.storage.list_files()
