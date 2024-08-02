import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.interface.file_interface import FileInterface
from src.core.key_manager import KeyManager

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk
import tempfile

class FileSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File System Manager")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        
        self.file_interface = None
        self.style = ttk.Style()
        self.style.theme_use('equilux')  # Using a modern dark theme
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Deployment Section
        deploy_frame = ttk.LabelFrame(main_frame, text="File System Deployment", padding="10 10 10 10")
        deploy_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(deploy_frame, text="Encryption Password:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(deploy_frame, show="*")
        self.password_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        self.deploy_button = ttk.Button(deploy_frame, text="Deploy File System", command=self.deploy_file_system)
        self.deploy_button.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        # File Operations Section
        operations_frame = ttk.LabelFrame(main_frame, text="File Operations", padding="10 10 10 10")
        operations_frame.pack(fill=tk.BOTH, expand=True)
        
        # Upload
        ttk.Label(operations_frame, text="File ID for Upload:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.upload_id_entry = ttk.Entry(operations_frame)
        self.upload_id_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        self.upload_button = ttk.Button(operations_frame, text="Upload File", command=self.upload_file)
        self.upload_button.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Download
        ttk.Label(operations_frame, text="File ID for Download:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.download_id_entry = ttk.Entry(operations_frame)
        self.download_id_entry.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        self.download_button = ttk.Button(operations_frame, text="Download File", command=self.download_file)
        self.download_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        # Delete
        ttk.Label(operations_frame, text="File ID for Deletion:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.delete_id_entry = ttk.Entry(operations_frame)
        self.delete_id_entry.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        self.delete_button = ttk.Button(operations_frame, text="Delete File", command=self.delete_file)
        self.delete_button.grid(row=5, column=0, columnspan=2, pady=(0, 10))
        
        # List Files
        self.list_button = ttk.Button(operations_frame, text="List Files", command=self.list_files)
        self.list_button.grid(row=6, column=0, columnspan=2, pady=(0, 10))

        # Base64 Retrieval
        ttk.Label(operations_frame, text="File ID for Base64 Retrieval:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.base64_id_entry = ttk.Entry(operations_frame)
        self.base64_id_entry.grid(row=7, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        self.base64_button = ttk.Button(operations_frame, text="Get File as Base64", command=self.get_file_base64)
        self.base64_button.grid(row=8, column=0, columnspan=2, pady=(0, 10))

        # Output Section
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10 10 10 10")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        self.output_text = tk.Text(output_frame, height=10, width=50, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure grid
        operations_frame.columnconfigure(1, weight=1)
        
    def deploy_file_system(self):
        password = self.password_entry.get()
        if not password:
            self.show_error("Please enter the encryption password.")
            return
        base_directory = filedialog.askdirectory(title="Select Directory for File System")
        if not base_directory:
            self.show_error("Please select a directory.")
            return
        
        try:
            key_manager = KeyManager(password)
            encryption_key = key_manager.get_key()
            self.file_interface = FileInterface(base_directory, encryption_key)
            self.show_info("File system deployed successfully!")
            self.status_var.set("File system deployed")
        except Exception as e:
            self.show_error(str(e))
        
    def upload_file(self):
        if not self.file_interface:
            self.show_error("File system not deployed.")
            return
        
        file_id = self.upload_id_entry.get()
        if not file_id:
            self.show_error("Please enter the file ID.")
            return
        
        file_path = filedialog.askopenfilename(title="Select File to Upload")
        if not file_path:
            self.show_error("Please select a file.")
            return
        
        try:
            self.file_interface.upload_file(file_path, file_id)
            self.show_info(f"File uploaded with ID: {file_id}")
            self.status_var.set(f"File uploaded: {file_id}")
        except Exception as e:
            self.show_error(str(e))
        
    def download_file(self):
        if not self.file_interface:
            self.show_error("File system not deployed.")
            return
        
        file_id = self.download_id_entry.get()
        if not file_id:
            self.show_error("Please enter the file ID.")
            return
        
        try:
            file_data = self.file_interface.download_file(file_id)
            destination_path = filedialog.asksaveasfilename(defaultextension=".dec", title="Save File As")
            if destination_path:
                with open(destination_path, 'wb') as file:
                    file.write(file_data)
                self.show_info(f"File saved to: {destination_path}")
                self.status_var.set(f"File downloaded: {file_id}")
            else:
                self.show_info("Download cancelled.")
        except Exception as e:
            self.show_error(str(e))
        
    def delete_file(self):
        if not self.file_interface:
            self.show_error("File system not deployed.")
            return
        
        file_id = self.delete_id_entry.get()
        if not file_id:
            self.show_error("Please enter the file ID.")
            return
        
        try:
            self.file_interface.delete_file(file_id)
            self.show_info(f"File with ID {file_id} deleted.")
            self.status_var.set(f"File deleted: {file_id}")
        except Exception as e:
            self.show_error(str(e))
        
    def list_files(self):
        if not self.file_interface:
            self.show_error("File system not deployed.")
            return
        
        try:
            files = self.file_interface.list_files()
            self.output_text.delete(1.0, tk.END)
            for file_id, file_data in files.items():
                self.output_text.insert(tk.END, f"File ID: {file_id}\n")
            self.status_var.set("File list updated")
        except Exception as e:
            self.show_error(str(e))

    def get_file_base64(self):
        if not self.file_interface:
            self.show_error("File system not deployed.")
            return
        
        file_id = self.base64_id_entry.get()
        if not file_id:
            self.show_error("Please enter the file ID.")
            return
        
        try:
            base64_data = self.file_interface.get_file_data_base64(file_id)
            # Display Base64 string in the output area
            output_text = f"File ID: {file_id}\nBase64 Data:\n{base64_data}"
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, output_text)
            self.status_var.set(f"Base64 data retrieved for ID: {file_id}")

            # Save log to a temporary file in the same directory as the application
            app_dir = os.path.dirname(os.path.abspath(__file__))
            with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=app_dir, prefix='base64_log_', suffix='.txt') as temp_file:
                temp_file.write(output_text)
                temp_file_path = temp_file.name

            self.status_var.set(f"Base64 data retrieved for ID: {file_id} and saved to {temp_file_path}")
        except Exception as e:
            self.show_error(str(e))
        
    def show_error(self, message):
        messagebox.showerror("Error", message)
        self.status_var.set("Error: " + message)
        
    def show_info(self, message):
        messagebox.showinfo("Info", message)
        self.status_var.set(message)

if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = FileSystemApp(root)
    root.mainloop()
