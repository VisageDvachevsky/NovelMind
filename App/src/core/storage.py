import os
import json
from .encryption import AdvancedEncryptor

class SecureStorage:
    def __init__(self, base_path, master_password):
        self.base_path = base_path
        self.index_file = os.path.join(base_path, 'index.enc')
        self.encryptor = AdvancedEncryptor()
        self.master_password = master_password
        self.index = self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.encryptor.decrypt(encrypted_data, self.master_password)
            return json.loads(decrypted_data)
        return {}

    def _save_index(self):
        index_data = json.dumps(self.index).encode()
        encrypted_data = self.encryptor.encrypt(index_data, self.master_password)
        with open(self.index_file, 'wb') as f:
            f.write(encrypted_data)

    def add_file(self, file_id, encrypted_path):
        self.index[file_id] = encrypted_path
        self._save_index()

    def get_file_path(self, file_id):
        return self.index.get(file_id)

    def remove_file(self, file_id):
        if file_id in self.index:
            del self.index[file_id]
            self._save_index()

    def list_files(self):
        return list(self.index.keys())