import os
from .encryption import AdvancedEncryptor
from .utils import create_directory_if_not_exists
from src.LogSystem.LoggerSystem import Logger

logger = Logger(use_json=True)
log_class = logger.log_class()

@log_class
class FileSystemInitializer:
    def __init__(self, base_path: str, master_password: str) -> None:

        self.base_path = base_path
        self.master_password = master_password

    def initialize(self) -> None:
        create_directory_if_not_exists(self.base_path)
        self._initialize_encryption()
        self._create_empty_index()

    def _initialize_encryption(self) -> None:
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
        index_file = os.path.join(self.base_path, 'index.enc')
        if not os.path.exists(index_file):
            encryptor = AdvancedEncryptor()
            empty_index = encryptor.encrypt(b'{}', self.master_password)
            with open(index_file, 'wb') as f:
                f.write(empty_index)
