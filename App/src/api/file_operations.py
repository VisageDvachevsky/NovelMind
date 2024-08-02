from core.file_handler import SecureFileHandler

class FileOperations:
    def __init__(self, file_handler: SecureFileHandler):
        self.file_handler = file_handler

    def add_file(self, file_path, file_id):
        self.file_handler.add_file(file_path, file_id)

    def read_file(self, file_id, decode=False):
        return self.file_handler.read_file(file_id, decode)

    def delete_file(self, file_id):
        self.file_handler.delete_file(file_id)

    def list_files(self):
        return self.file_handler.list_files()