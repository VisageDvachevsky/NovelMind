from src.core.file_manager import FileManager
from src.core.utils import generate_unique_id
import base64
import lzma

class FileInterface:
    def __init__(self, base_directory: str, encryption_key: bytes):
        self.file_manager = FileManager(base_directory, encryption_key)

    def upload_file(self, file_path: str, file_id: str) -> None:
        """Encrypts and uploads a file to the system."""
        try:
            self.file_manager.add_file(file_path, file_id)
        except Exception as e:
            raise Exception(f"Failed to upload file: {e}")

    def download_file(self, file_id: str) -> bytes:
        """Retrieves and decrypts file data by its ID."""
        try:
            return self.file_manager.get_file_data(file_id)
        except Exception as e:
            raise Exception(f"Failed to download file: {e}")
        
    def get_file_data_base64(self, file_id: str) -> str:
        """Retrieves, compresses, and returns file data as a Base64-encoded string."""
        try:
            file_data = self.download_file(file_id)
            compressed_data = lzma.compress(file_data)
            return base64.b64encode(compressed_data).decode('utf-8')
        except Exception as e:
            raise Exception(f"Failed to get file data as Base64: {e}")
        
    def delete_file(self, file_id: str) -> None:
        """Deletes a file from the system."""
        try:
            self.file_manager.delete_file(file_id)
        except Exception as e:
            raise Exception(f"Failed to delete file: {e}")

    def list_files(self) -> dict:
        """Lists all files with their IDs and data."""
        return self.file_manager.list_files()

    def generate_file_id(self) -> str:
        """Generates a unique file ID."""
        return generate_unique_id()