import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import logging
from src.core.encryption import EncryptionManager
from src.interfaces.file_interface import FileInterface

class FileUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Management")
        self.file_path = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Storage Path:").grid(row=0, column=0, padx=10, pady=5)
        self.storage_path_entry = tk.Entry(self.root)
        self.storage_path_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Select File", command=self.select_file).grid(row=1, column=0, columnspan=2, pady=10)
        self.file_path_label = tk.Label(self.root, text="No file selected")
        self.file_path_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.root, text="Upload File", command=self.upload_file).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Download File", command=self.download_file).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Delete File", command=self.delete_file).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Check Integrity", command=self.check_file_integrity).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="List Files", command=self.list_files).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Get File Info", command=self.get_file_info).grid(row=8, column=0, columnspan=2, pady=10)

        self.output_text = tk.Text(self.root, height=10, width=50)
        self.output_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path
            self.file_path_label.config(text=file_path)
        else:
            self.file_path = None
            self.file_path_label.config(text="No file selected")

    def upload_file(self):
        storage_path = self.storage_path_entry.get()
        file_path = self.file_path

        if not storage_path or not file_path:
            messagebox.showerror("Error", "Please provide all inputs.")
            return

        try:
            data_key = EncryptionManager.generate_key()
            metadata_key = EncryptionManager.generate_key()

            file_interface = FileInterface(storage_path)
            file_id = file_interface.upload_file(file_path, data_key, metadata_key)

            if file_id:
                self.root.clipboard_clear()
                self.root.clipboard_append(file_id)
                messagebox.showinfo("Success", f"File uploaded with ID: {file_id} (copied to clipboard)")
            else:
                messagebox.showerror("Error", "Failed to upload file.")
        except Exception as e:
            logging.error(f"Error uploading file: {e}")
            messagebox.showerror("Error", str(e))

    def download_file(self):
        file_id = self.prompt_for_file_id()
        storage_path = self.storage_path_entry.get()

        if not storage_path or not file_id:
            messagebox.showerror("Error", "Please provide all inputs.")
            return

        try:
            data_key = EncryptionManager.generate_key()
            metadata_key = EncryptionManager.generate_key()

            file_interface = FileInterface(storage_path)
            data = file_interface.download_file(file_id, data_key, metadata_key)

            if data:
                with open(f"downloaded_{file_id}", "wb") as file:
                    file.write(data)
                messagebox.showinfo("Success", f"File downloaded and saved as downloaded_{file_id}")
            else:
                messagebox.showerror("Error", "File not found.")
        except Exception as e:
            logging.error(f"Error downloading file: {e}")
            messagebox.showerror("Error", str(e))

    def delete_file(self):
        file_id = self.prompt_for_file_id()
        storage_path = self.storage_path_entry.get()

        if not storage_path or not file_id:
            messagebox.showerror("Error", "Please provide all inputs.")
            return

        try:
            data_key = EncryptionManager.generate_key()
            metadata_key = EncryptionManager.generate_key()

            file_interface = FileInterface(storage_path)
            file_interface.delete_file(file_id, data_key, metadata_key)

            messagebox.showinfo("Success", f"File with ID {file_id} deleted.")
        except Exception as e:
            logging.error(f"Error deleting file: {e}")
            messagebox.showerror("Error", str(e))

    def check_file_integrity(self):
        file_id = self.prompt_for_file_id()
        storage_path = self.storage_path_entry.get()

        if not storage_path or not file_id:
            messagebox.showerror("Error", "Please provide all inputs.")
            return

        try:
            data_key = EncryptionManager.generate_key()
            metadata_key = EncryptionManager.generate_key()

            file_interface = FileInterface(storage_path)
            integrity = file_interface.check_file_integrity(file_id, data_key, metadata_key)

            self.output_text.insert(tk.END, f"File integrity check: {'Valid' if integrity else 'Invalid'}\n")
        except Exception as e:
            logging.error(f"Error checking file integrity: {e}")
            messagebox.showerror("Error", str(e))

    def list_files(self):
        storage_path = self.storage_path_entry.get()

        if not storage_path:
            messagebox.showerror("Error", "Please provide all inputs.")
            return

        try:
            data_key = EncryptionManager.generate_key()
            metadata_key = EncryptionManager.generate_key()

            file_interface = FileInterface(storage_path)
            file_ids = file_interface.list_files(data_key, metadata_key)

            self.output_text.insert(tk.END, f"Accessible Files: {', '.join(file_ids)}\n")
        except Exception as e:
            logging.error(f"Error listing files: {e}")
            messagebox.showerror("Error", str(e))

    def get_file_info(self):
        file_id = self.prompt_for_file_id()
        storage_path = self.storage_path_entry.get()

        if not storage_path or not file_id:
            messagebox.showerror("Error", "Please provide all inputs.")
            return

        try:
            data_key = EncryptionManager.generate_key()
            metadata_key = EncryptionManager.generate_key()

            file_interface = FileInterface(storage_path)
            metadata = file_interface.get_file_info(file_id, data_key, metadata_key)

            if metadata:
                self.output_text.insert(tk.END, f"File ID: {file_id}\nMetadata: {metadata}\n")
            else:
                self.output_text.insert(tk.END, "File metadata not found.\n")
        except Exception as e:
            logging.error(f"Error getting file info: {e}")
            messagebox.showerror("Error", str(e))

    def prompt_for_file_id(self):
        return simpledialog.askstring("File ID", "Enter the file ID:")

def run():
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    app = FileUploaderApp(root)
    root.mainloop()
