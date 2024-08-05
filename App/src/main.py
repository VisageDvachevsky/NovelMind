from api.system_operation import SystemOperations
from api.file_operations import FileOperations
import base64
import getpass
import tempfile
import os

def get_valid_password():
    while True:
        password = getpass.getpass("Enter the master password for the file system (8 characters minimum): ")
        if len(password) >= 8:
            return password
        print("Password must be at least 8 characters long. Please try again.")

def print_file_structure(structure, indent=""):
    for name, info in structure["contents"].items():
        if info["type"] == "directory":
            print(f"{indent}{name}/")
            print_file_structure(info, indent + "  ")
        else:
            print(f"{indent}{name}")

def main():
    base_path = os.path.abspath(input("Enter the path to deploy the file system: "))
    os.makedirs(base_path, exist_ok=True)
    os.chdir(base_path)
    master_password = get_valid_password()

    try:
        file_handler = SystemOperations.deploy(base_path, master_password)
        file_ops = FileOperations(file_handler)

        print("File system deployed successfully!")

        while True:
            current_dir = file_ops.get_current_directory()
            print(f"\nCurrent directory: {current_dir}")
            print("1. Add file")
            print("2. Read file")
            print("3. Delete file")
            print("4. List files")
            print("5. Create directory")
            print("6. Rename directory")
            print("7. Delete directory")
            print("8. Move file")
            print("9. Change directory")
            print("10. Exit")

            choice = input("Enter your choice (1-10): ")

            if choice == '1':
                file_path = input("Enter the path of the file to add: ")
                file_id = input("Enter the file ID: ")
                file_ops.add_file(file_path, file_id)
                print("File added successfully!")

            elif choice == '2':
                file_id = input("Enter the file ID to read: ")
                decode = input("Attempt to decode the file? (y/n): ").lower() == 'y'
                content = file_ops.read_file(file_id, decode)

                if decode:
                    print("File content:", content)
                else:
                    encoded_content = base64.b64encode(content).decode('utf-8')
                    if len(encoded_content) > 1000:
                        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
                            temp_file.write(encoded_content)
                            temp_file_path = temp_file.name
                        print(f"File content is too long. Saved encoded content to {temp_file_path}")
                    else:
                        print("File content (base64 encoded):", encoded_content)

            elif choice == '3':
                file_id = input("Enter the file ID to delete: ")
                file_ops.delete_file(file_id)
                print("File deleted successfully!")

            elif choice == '4':
                file_structure = file_ops.list_files()
                print("File system structure:")
                print_file_structure(file_structure)

            elif choice == '5':
                dir_name = input("Enter the name of the directory to create: ")
                file_ops.create_directory(dir_name)
                print("Directory created successfully!")

            elif choice == '6':
                old_name = input("Enter the current name of the directory: ")
                new_name = input("Enter the new name for the directory: ")
                file_ops.rename_directory(old_name, new_name)
                print("Directory renamed successfully!")

            elif choice == '7':
                dir_name = input("Enter the name of the directory to delete: ")
                file_ops.delete_directory(dir_name)
                print("Directory deleted successfully!")

            elif choice == '8':
                file_id = input("Enter the ID of the file to move: ")
                dest_dir = input("Enter the name of the destination directory: ")
                file_ops.move_file(file_id, dest_dir)
                print("File moved successfully!")

            elif choice == '9':
                dir_name = input("Enter the name of the directory to change to (use '..' to go up): ")
                file_ops.change_directory(dir_name)
                print(f"Changed to directory: {file_ops.get_current_directory()}")

            elif choice == '10':
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()