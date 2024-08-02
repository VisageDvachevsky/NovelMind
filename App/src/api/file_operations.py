from core.file_handler import SecureFileHandler
from typing import Optional, List

class FileOperations:
    """
    A class to perform file operations such as adding, reading, deleting, and listing files.
    """

    def __init__(self, file_handler: SecureFileHandler) -> None:
        """
        Initialize the FileOperations with a SecureFileHandler instance.

        :param file_handler: An instance of SecureFileHandler to manage secure file operations.
        """
        self.file_handler = file_handler

    def add_file(self, file_path: str, file_id: str) -> None:
        """
        Add a file to secure storage.

        :param file_path: The path to the file to be added.
        :param file_id: The unique identifier for the file.
        """
        self.file_handler.add_file(file_path, file_id)

    def read_file(self, file_id: str, decode: bool = False) -> str:
        """
        Read a file from secure storage.

        :param file_id: The unique identifier for the file.
        :param decode: Whether to decode the decrypted content as a UTF-8 string or base64.
        :return: The decrypted content as a string.
        :raises FileNotFoundError: If the file with the specified ID is not found.
        """
        return self.file_handler.read_file(file_id, decode)

    def delete_file(self, file_id: str) -> None:
        """
        Delete a file from secure storage.

        :param file_id: The unique identifier for the file.
        :raises FileNotFoundError: If the file with the specified ID is not found.
        """
        self.file_handler.delete_file(file_id)

    def list_files(self) -> List[str]:
        """
        List all stored file IDs.

        :return: A list of file IDs.
        """
        return self.file_handler.list_files()
