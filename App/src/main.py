from api.system_operation import SystemOperations
from api.file_operations import FileOperations
import base64

def get_valid_password():
    while True:
        password = input("Enter the master password for the file system (8 characters): ")
        if len(password) == 8:
            return password
        print("Password must be exactly 8 characters long. Please try again.")

def main():
    base_path = input("Enter the path to deploy the file system: ")
    master_password = get_valid_password()
    
    try:
        file_handler = SystemOperations.deploy(base_path, master_password)
        file_ops = FileOperations(file_handler)
        
        print("File system deployed successfully!")
        
        while True:
            print("\n1. Add file")
            print("2. Read file")
            print("3. Delete file")
            print("4. List files")
            print("5. Exit")
            
            choice = input("Enter your choice (1-5): ")
            
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
                    print("File content (base64 encoded):", base64.b64encode(content).decode('utf-8'))
                    save_path = input("Enter path to save the file (or press Enter to skip): ")
                    if save_path:
                        with open(save_path, 'wb') as f:
                            f.write(content)
                        print(f"File saved to {save_path}")
            
            elif choice == '3':
                file_id = input("Enter the file ID to delete: ")
                file_ops.delete_file(file_id)
                print("File deleted successfully!")
            
            elif choice == '4':
                files = file_ops.list_files()
                print("Files in the system:", files)
            
            elif choice == '5':
                print("Exiting...")
                break
            
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()