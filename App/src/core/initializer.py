import os
from .encryption import AdvancedEncryptor
from .utils import create_directory_if_not_exists
from LogSystem.LoggerSystem import Logger

logger = Logger(use_json=True)
log_class = logger.log_class()

@log_class
class FileSystemInitializer:
    """
    A class to initialize the file system for secure storage.
    """

    def __init__(self, base_path: str, master_password: str) -> None:
        """
        Initialize the FileSystemInitializer with the base path and master password.

        :param base_path: The base directory path for storage initialization.
        :param master_password: The master password for encryption and decryption.
        """
        self.base_path = base_path
        self.master_password = master_password

    def initialize(self) -> None:
        """
        Perform the initialization steps for the file system.
        """
        create_directory_if_not_exists(self.base_path)
        self._initialize_encryption()
        self._create_empty_index()

    def _initialize_encryption(self) -> None:
        """
        Initialize the encryption by creating key and salt files if they do not exist.
        """
        encryptor = AdvancedEncryptor()
        key_file = os.path.join(self.base_path, 'master_key.key')
        salt_file = os.path.join(self.base_path, 'salt.key')
        
        if not os.path.exists(key_file):
            with open(key_file, 'wb') as f:
                f.write(encryptor.master_key)
        
        if not os.path.exists(salt_file):
            with open(salt_file, 'wb') as f:
                f.write(encryptor.salt)

    def _create_empty_index(self) -> None:
        """
        Create an empty index file for storing file metadata if it does not exist.
        """
        index_file = os.path.join(self.base_path, 'index.enc')
        if not os.path.exists(index_file):
            encryptor = AdvancedEncryptor()
            empty_index = encryptor.encrypt(b'{}', self.master_password)
            with open(index_file, 'wb') as f:
                f.write(empty_index)
