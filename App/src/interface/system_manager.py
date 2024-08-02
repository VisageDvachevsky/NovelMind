from src.interface.file_interface import FileInterface

class SystemManager:
    def __init__(self, admin_password: str, base_directory: str = None):
        # Initialize the file interface with the provided or default base directory
        self.file_interface = FileInterface(admin_password, base_directory)

    def upload_file(self, file_path: str, file_id: str) -> None:
        """Handles the uploading of a file."""
        self.file_interface.upload_file(file_path, file_id)

    def get_file(self, file_id: str) -> bytes:
        """Handles the retrieval of a file."""
        return self.file_interface.get_file(file_id)

    def save_file_temp(self, file_id: str) -> str:
        """Handles the retrieval and saving of a file as a temporary file."""
        return self.file_interface.save_file_temp(file_id)

    def delete_file(self, file_id: str) -> None:
        """Handles the deletion of a file."""
        self.file_interface.delete_file(file_id)

    def get_base_directory(self) -> str:
        """Returns the base directory path."""
        return self.file_interface.get_base_directory()