import os
import json
from typing import Dict, Any
from .encryption import AdvancedEncryptor
from src.LogSystem.LoggerSystem import Logger

logger = Logger(use_json=True)
log_class = logger.log_class()

@log_class
class SecureStorage:
    def __init__(self, base_path: str, master_password: str) -> None:
        self.base_path = base_path
        self.index_file = os.path.join(base_path, 'index.enc')
        self.encryptor = AdvancedEncryptor()
        self.master_password = master_password
        self.index = self._load_index()
        if "root" not in self.index:
            self.index["root"] = {"type": "directory", "contents": {}}

    def _load_index(self) -> Dict[str, Any]:
        if os.path.exists(self.index_file):
            with open(self.index_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.encryptor.decrypt(encrypted_data, self.master_password)
            return json.loads(decrypted_data)
        return {}

    def _save_index(self) -> None:
        index_data = json.dumps(self.index).encode()
        encrypted_data = self.encryptor.encrypt(index_data, self.master_password)
        with open(self.index_file, 'wb') as f:
            f.write(encrypted_data)

    def add_file(self, file_path: str, encrypted_path: str) -> None:
        parts = file_path.split('/')
        current = self.index["root"]["contents"]
        for part in parts[:-1]:
            if part:
                if part not in current:
                    current[part] = {"type": "directory", "contents": {}}
                current = current[part]["contents"]
        current[parts[-1]] = {"type": "file", "path": encrypted_path}
        self._save_index()

    def get_file_path(self, file_path: str) -> str:
        parts = file_path.split('/')
        current = self.index["root"]["contents"]
        for part in parts[:-1]:
            if part:
                if part not in current or current[part]["type"] != "directory":
                    return None
                current = current[part]["contents"]
        if parts[-1] in current and current[parts[-1]]["type"] == "file":
            return current[parts[-1]]["path"]
        return None

    def remove_file(self, file_path: str) -> None:
        parts = file_path.split('/')
        current = self.index["root"]["contents"]
        for part in parts[:-1]:
            if part:
                if part not in current or current[part]["type"] != "directory":
                    return
                current = current[part]["contents"]
        if parts[-1] in current and current[parts[-1]]["type"] == "file":
            del current[parts[-1]]
            self._save_index()

    def get_file_structure(self) -> Dict[str, Any]:
        return self.index["root"]

    def create_directory(self, dir_path: str) -> None:
        parts = dir_path.split('/')
        current = self.index["root"]["contents"]
        for part in parts:
            if part:
                if part not in current:
                    current[part] = {"type": "directory", "contents": {}}
                current = current[part]["contents"]
        self._save_index()

    def rename_directory(self, old_path: str, new_path: str) -> None:
        old_parts = old_path.split('/')
        new_parts = new_path.split('/')
        old_parent = self.index["root"]["contents"]
        new_parent = self.index["root"]["contents"]
        for part in old_parts[:-1]:
            if part:
                old_parent = old_parent[part]["contents"]
        for part in new_parts[:-1]:
            if part:
                if part not in new_parent:
                    new_parent[part] = {"type": "directory", "contents": {}}
                new_parent = new_parent[part]["contents"]
        if old_parts[-1] in old_parent and old_parent[old_parts[-1]]["type"] == "directory":
            new_parent[new_parts[-1]] = old_parent.pop(old_parts[-1])
            self._save_index()

    def delete_directory(self, dir_path: str) -> None:
        parts = dir_path.split('/')
        current = self.index["root"]["contents"]
        for part in parts[:-1]:
            if part:
                if part not in current or current[part]["type"] != "directory":
                    return
                current = current[part]["contents"]
        if parts[-1] in current and current[parts[-1]]["type"] == "directory":
            del current[parts[-1]]
            self._save_index()

    def move_file(self, src_path: str, dest_path: str) -> None:
        src_parts = src_path.split('/')
        dest_parts = dest_path.split('/')
        src_parent = self.index["root"]["contents"]
        dest_parent = self.index["root"]["contents"]
        for part in src_parts[:-1]:
            if part:
                src_parent = src_parent[part]["contents"]
        for part in dest_parts[:-1]:
            if part:
                if part not in dest_parent:
                    dest_parent[part] = {"type": "directory", "contents": {}}
                dest_parent = dest_parent[part]["contents"]
        if src_parts[-1] in src_parent and src_parent[src_parts[-1]]["type"] == "file":
            dest_parent[dest_parts[-1]] = src_parent.pop(src_parts[-1])
            self._save_index()

    def directory_exists(self, dir_path: str) -> bool:
        parts = dir_path.split('/')
        current = self.index["root"]["contents"]
        for part in parts:
            if part:
                if part not in current or current[part]["type"] != "directory":
                    return False
                current = current[part]["contents"]
        return True