import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import base64
import tempfile
import threading
import os
from api.system_operation import SystemOperations
from api.file_operations import FileOperations

class PasswordDialog(ctk.CTk):
    def __init__(self, title="Password", prompt="Enter password:", min_length=8):
        super().__init__()
        self.title(title)
        self.geometry("300x150")

        self.password = None
        self.min_length = min_length

        prompt_label = ctk.CTkLabel(self, text=prompt)
        prompt_label.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=5)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ok_button = ctk.CTkButton(button_frame, text="OK", command=self.ok)
        ok_button.pack(side=tk.LEFT, padx=5)

        cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side=tk.RIGHT, padx=5)

    def ok(self):
        password = self.password_entry.get()
        if len(password) < self.min_length:
            messagebox.showerror("Error", f"Password must be at least {self.min_length} characters long.")
        else:
            self.password = password
            self.destroy()

    def cancel(self):
        self.password = None
        self.destroy()

    def get_password(self):
        self.mainloop()
        return self.password

class FileManagerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Secure File Manager")
        self.geometry("800x600")

        self.file_ops = None
        self.current_dir = ""

        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)

        self.current_dir_label = ctk.CTkLabel(top_frame, text="Current Directory: Not deployed")
        self.current_dir_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.deploy_button = ctk.CTkButton(top_frame, text="Deploy File System", command=self.deploy_file_system)
        self.deploy_button.grid(row=0, column=1, padx=5, pady=5)

        self.file_list = ctk.CTkTextbox(main_frame, wrap="none")
        self.file_list.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        bottom_frame = ctk.CTkFrame(main_frame)
        bottom_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        buttons = [
            ("Add File", self.add_file),
            ("Read File", self.read_file),
            ("Delete File", self.delete_file),
            ("Create Directory", self.create_directory),
            ("Rename Directory", self.rename_directory),
            ("Delete Directory", self.delete_directory),
            ("Move File", self.move_file),
            ("Change Directory", self.change_directory),
        ]

        for i, (text, command) in enumerate(buttons):
            button = ctk.CTkButton(bottom_frame, text=text, command=command)
            button.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="ew")

    def deploy_file_system(self):
        def task():
            base_path = filedialog.askdirectory(title="Select directory to deploy file system")
            if not base_path:
                return

            password_dialog = PasswordDialog()
            password = password_dialog.get_password()
            if not password:
                return

            try:
                os.chdir(base_path)
                file_handler = SystemOperations.deploy(base_path, password)
                self.file_ops = FileOperations(file_handler)
                self.current_dir = self.file_ops.get_current_directory()
                self.update_file_list()
                self.deploy_button.configure(state="disabled")
                messagebox.showinfo("Success", "File system deployed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to deploy file system: {str(e)}")

        threading.Thread(target=task).start()

    def update_file_list(self):
        def task():
            self.current_dir_label.configure(text=f"Current Directory: {self.current_dir}")
            self.file_list.delete("1.0", tk.END)
            if self.file_ops:
                file_structure = self.file_ops.list_files()
                self.print_file_structure(file_structure)

        threading.Thread(target=task).start()

    def print_file_structure(self, structure, indent=""):
        for name, info in structure["contents"].items():
            if info["type"] == "directory":
                self.file_list.insert(tk.END, f"{indent}{name}/\n")
                self.print_file_structure(info, indent + "  ")
            else:
                self.file_list.insert(tk.END, f"{indent}{name}\n")

    def add_file(self):
        def task():
            if not self.file_ops:
                messagebox.showerror("Error", "File system not deployed")
                return

            file_path = filedialog.askopenfilename(title="Select file to add")
            if not file_path:
                return

            file_id = ctk.CTkInputDialog(text="Enter the file ID:", title="File ID").get_input()
            if not file_id:
                return

            try:
                self.file_ops.add_file(file_path, file_id)
                self.update_file_list()
                messagebox.showinfo("Success", "File added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add file: {str(e)}")

        threading.Thread(target=task).start()

    def read_file(self):
        def task():
            if not self.file_ops:
                messagebox.showerror("Error", "File system not deployed")
                return

            file_id = ctk.CTkInputDialog(text="Enter the file ID to read:", title="Read File").get_input()
            if not file_id:
                return

            try:
                content = self.file_ops.read_file(file_id, decode=False)
                encoded_content = base64.b64encode(content).decode('utf-8')

                if len(encoded_content) > 1000:
                    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
                        temp_file.write(encoded_content)
                        temp_file_path = temp_file.name
                    messagebox.showinfo("File Content", f"File content is too long. Saved encoded content to {temp_file_path}")
                else:
                    messagebox.showinfo("File Content", f"File content (base64 encoded):\n{encoded_content}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")

        threading.Thread(target=task).start()

    def delete_file(self):
        def task():
            if not self.file_ops:
                messagebox.showerror("Error", "File system not deployed")
                return

            file_id = ctk.CTkInputDialog(text="Enter the file ID to delete:", title="Delete File").get_input()
            if not file_id:
                return

            try:
                self.file_ops.delete_file(file_id)
                self.update_file_list()
                messagebox.showinfo("Success", "File deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file: {str(e)}")

        threading.Thread(target=task).start()

    def create_directory(self):
        def task():
            if not self.file_ops:
                messagebox.showerror("Error", "File system not deployed")
                return

            dir_name = ctk.CTkInputDialog(text="Enter the name of the directory to create:", title="Create Directory").get_input()
            if not dir_name:
                return

            try:
                self.file_ops.create_directory(dir_name)
                self.update_file_list()
                messagebox.showinfo("Success", "Directory created successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create directory: {str(e)}")

        threading.Thread(target=task).start()

    def rename_directory(self):
        def task():
            if not self.file_ops:
                messagebox.showerror("Error", "File system not deployed")
                return

            old_name = ctk.CTkInputDialog(text="Enter the current name of the directory:", title="Rename Directory").get_input()
            if not old_name:
                return

            new_name = ctk.CTkInputDialog(text="Enter the new name for the directory:", title="Rename Directory").get_input()
            if not new_name:
                return

            try:
                self.file_ops.rename_directory(old_name, new_name)
                self.update_file_list()
                messagebox.showinfo("Success", "Directory renamed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename directory: {str(e)}")

        threading.Thread(target=task).start()

    def delete_directory(self):
        def task():
            if not self.file_ops:
                messagebox.showerror("Error", "File system not deployed")
                return

            dir_name = ctk.CTkInputDialog(text="Enter the name of the directory to delete:", title="Delete Directory").get_input()
            if not dir_name:
                return

            try:
                self.file_ops.delete_directory(dir_name)
                self.update_file_list()
                messagebox.showinfo("Success", "Directory deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete directory: {str(e)}")

        threading.Thread(target=task).start()

    def move_file(self):
        def task():
            if not self.file_ops:
                messagebox.showerror("Error", "File system not deployed")
                return

            file_id = ctk.CTkInputDialog(text="Enter the ID of the file to move:", title="Move File").get_input()
            if not file_id:
                return

            dest_dir = ctk.CTkInputDialog(text="Enter the name of the destination directory:", title="Move File").get_input()
            if not dest_dir:
                return

            try:
                self.file_ops.move_file(file_id, dest_dir)
                self.update_file_list()
                messagebox.showinfo("Success", "File moved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to move file: {str(e)}")

        threading.Thread(target=task).start()

    def change_directory(self):
        def task():
            if not self.file_ops:
                messagebox.showerror("Error", "File system not deployed")
                return

            dir_name = ctk.CTkInputDialog(text="Enter the name of the directory to change to (use '..' to go up):", title="Change Directory").get_input()
            if not dir_name:
                return

            try:
                self.file_ops.change_directory(dir_name)
                self.current_dir = self.file_ops.get_current_directory()
                self.update_file_list()
                messagebox.showinfo("Success", f"Changed to directory: {self.current_dir}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change directory: {str(e)}")

        threading.Thread(target=task).start()

if __name__ == "__main__":
    app = FileManagerGUI()
    app.mainloop()
