import os
import base64
from .encryption import AdvancedEncryptor
from .storage import SecureStorage

class SecureFileHandler:
    def __init__(self, base_path, master_password):
        self.base_path = base_path
        self.encryptor = AdvancedEncryptor()
        self.storage = SecureStorage(base_path, master_password)
        self.master_password = master_password

    def add_file(self, file_path, file_id):
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        encrypted_content = self.encryptor.encrypt(file_content, self.master_password)
        encrypted_file_path = os.path.join(self.base_path, f'{file_id}.enc')
        
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_content)
        
        self.storage.add_file(file_id, encrypted_file_path)

    def read_file(self, file_id, decode=False):
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

    def delete_file(self, file_id):
        encrypted_file_path = self.storage.get_file_path(file_id)
        if not encrypted_file_path:
            raise FileNotFoundError(f"File with id {file_id} not found")

        os.remove(encrypted_file_path)
        self.storage.remove_file(file_id)

    def list_files(self):
        return self.storage.list_files()