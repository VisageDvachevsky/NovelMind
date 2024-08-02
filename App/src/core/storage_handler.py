import os

class StorageHandler:
    def __init__(self, base_directory: str):
        self.base_directory = base_directory
        if not os.path.exists(base_directory):
            os.makedirs(base_directory)

    def store_data(self, file_id: str, data: bytes) -> None:
        """Stores encrypted data in a file with a specific ID."""
        file_path = os.path.join(self.base_directory, f"{file_id}.enc")
        with open(file_path, 'wb') as file:
            file.write(data)

    def retrieve_data(self, file_id: str) -> bytes:
        """Retrieves encrypted data from a file by its ID."""
        file_path = os.path.join(self.base_directory, f"{file_id}.enc")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No file found with ID {file_id}")
        with open(file_path, 'rb') as file:
            return file.read()

    def delete_data(self, file_id: str) -> None:
        """Deletes the file associated with the given ID."""
        file_path = os.path.join(self.base_directory, f"{file_id}.enc")
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"No file found with ID {file_id}")