import os
import base64
from typing import Optional, List, Dict
from .encryption import AdvancedEncryptor
from .storage import SecureStorage
from src.LogSystem.LoggerSystem import Logger

logger = Logger(use_json=True)
log_class = logger.log_class()

@log_class
class SecureFileHandler:
    def __init__(self, base_path: str, master_password: str) -> None:
        self.base_path = base_path
        self.encryptor = AdvancedEncryptor()
        self.storage = SecureStorage(base_path, master_password)
        self.master_password = master_password

    def add_file(self, file_path: str, dest_path: str) -> None:
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        encrypted_content = self.encryptor.encrypt(file_content, self.master_password)
        file_id = os.path.basename(dest_path)
        encrypted_file_path = os.path.join(self.base_path, f'{file_id}.enc')
        
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_content)
        
        self.storage.add_file(dest_path, encrypted_file_path)

    def read_file(self, file_path: str, decode: bool = False) -> str:
        encrypted_file_path = self.storage.get_file_path(file_path)
        if not encrypted_file_path:
            raise FileNotFoundError(f"File not found: {file_path}")

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

    def delete_file(self, file_path: str) -> None:
        encrypted_file_path = self.storage.get_file_path(file_path)
        if not encrypted_file_path:
            raise FileNotFoundError(f"File not found: {file_path}")

        os.remove(encrypted_file_path)
        self.storage.remove_file(file_path)

    def list_files(self) -> Dict:
        return self.storage.get_file_structure()

    def create_directory(self, dir_path: str) -> None:
        self.storage.create_directory(dir_path)

    def rename_directory(self, old_path: str, new_path: str) -> None:
        self.storage.rename_directory(old_path, new_path)

    def delete_directory(self, dir_path: str) -> None:
        self.storage.delete_directory(dir_path)

    def move_file(self, src_path: str, dest_path: str) -> None:
        self.storage.move_file(src_path, dest_path)

    def directory_exists(self, dir_path: str) -> bool:
        return self.storage.directory_exists(dir_path)