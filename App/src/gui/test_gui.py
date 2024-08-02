import tkinter as tk
from tkinter import filedialog, messagebox
from src.core.encryption import EncryptionManager
from src.interfaces.file_interface import FileInterface

class FileUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Uploader")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="User ID:").grid(row=0, column=0, padx=10, pady=5)
        self.user_id_entry = tk.Entry(self.root)
        self.user_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Storage Path:").grid(row=1, column=0, padx=10, pady=5)
        self.storage_path_entry = tk.Entry(self.root)
        self.storage_path_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Select File", command=self.select_file).grid(row=2, column=0, columnspan=2, pady=10)
        self.file_path_label = tk.Label(self.root, text="No file selected")
        self.file_path_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.root, text="Upload File", command=self.upload_file).grid(row=4, column=0, columnspan=2, pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path
            self.file_path_label.config(text=file_path)
        else:
            self.file_path = None
            self.file_path_label.config(text="No file selected")

    def upload_file(self):
        user_id = self.user_id_entry.get()
        storage_path = self.storage_path_entry.get()
        file_path = self.file_path

        if not user_id or not storage_path or not file_path:
            messagebox.showerror("Error", "Please provide all inputs.")
            return

        try:
            data_key = EncryptionManager.generate_key()
            metadata_key = EncryptionManager.generate_key()

            file_interface = FileInterface(storage_path)
            file_id = file_interface.upload_file(file_path, user_id, data_key, metadata_key)

            messagebox.showinfo("Success", f"File uploaded with ID: {file_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def run():
    root = tk.Tk()
    app = FileUploaderApp(root)
    root.mainloop()
