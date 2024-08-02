# NovelEditor
Core Components
The core components include the following modules:

Encryption
File Handler
File System Initializer
Secure Storage
Utility Functions
API Components
The API components provide high-level operations for file management and system deployment:

File Operations
System Operations
Core Components
1. Encryption (encryption.py)
AdvancedEncryptor
A class to handle encryption and decryption of data using AES encryption.

Methods:
__init__(self, key_file: str = 'master_key.key', salt_file: str = 'salt.key') -> None: Initializes the AdvancedEncryptor with specified key and salt files.
_load_or_generate_key(self, file_path: str) -> bytes: Loads an existing key from the file path or generates a new key if the file does not exist.
_derive_key(self, password: str) -> bytes: Derives a cryptographic key from a password using PBKDF2 HMAC.
encrypt(self, data: bytes, password: str) -> bytes: Encrypts the provided data using the derived key from the password.
decrypt(self, encrypted_data: bytes, password: str) -> bytes: Decrypts the provided encrypted data using the derived key from the password.
2. File Handler (file_handler.py)
SecureFileHandler
A class to handle secure file operations such as adding, reading, deleting, and listing files.

Methods:
__init__(self, base_path: str, master_password: str) -> None: Initializes the SecureFileHandler with the base path and master password.
add_file(self, file_path: str, file_id: str) -> None: Adds and encrypts a file with a given file ID.
read_file(self, file_id: str, decode: bool = False) -> str: Reads and decrypts a file by its file ID.
delete_file(self, file_id: str) -> None: Deletes a file by its file ID.
list_files(self) -> List[str]: Lists all stored file IDs.
3. File System Initializer (initializer.py)
FileSystemInitializer
A class to initialize the file system for secure storage.

Methods:
__init__(self, base_path: str, master_password: str) -> None: Initializes the FileSystemInitializer with the base path and master password.
initialize(self) -> None: Performs the initialization steps for the file system.
_initialize_encryption(self) -> None: Initializes the encryption by creating key and salt files if they do not exist.
_create_empty_index(self) -> None: Creates an empty index file for storing file metadata if it does not exist.
4. Secure Storage (storage.py)
SecureStorage
A class to handle secure storage and retrieval of file metadata.

Methods:
__init__(self, base_path: str, master_password: str) -> None: Initializes the SecureStorage with the base path and master password.
_load_index(self) -> Dict[str, str]: Loads the file index from the encrypted index file.
_save_index(self) -> None: Saves the current file index to the encrypted index file.
add_file(self, file_id: str, encrypted_path: str) -> None: Adds a file to the index.
get_file_path(self, file_id: str) -> Optional[str]: Gets the file path of a file by its file ID.
remove_file(self, file_id: str) -> None: Removes a file from the index.
list_files(self) -> List[str]: Lists all stored file IDs.
5. Utility Functions (utils.py)
Functions:
create_directory_if_not_exists(path: str) -> None: Creates a directory if it does not already exist.
is_valid_path(path: str) -> bool: Checks if a path is a valid directory path.
API Components
1. File Operations (file_operations.py)
FileOperations
A class to perform file operations such as adding, reading, deleting, and listing files.

Methods:
__init__(self, file_handler: SecureFileHandler) -> None: Initializes the FileOperations with a SecureFileHandler instance.
add_file(self, file_path: str, file_id: str) -> None: Adds a file to secure storage.
read_file(self, file_id: str, decode: bool = False) -> str: Reads a file from secure storage.
delete_file(self, file_id: str) -> None: Deletes a file from secure storage.
list_files(self) -> List[str]: Lists all stored file IDs.
2. System Operations (system_operations.py)
SystemOperations
A class to perform system operations such as deploying the file system.

Methods:
deploy(base_path: str, master_password: str) -> SecureFileHandler: Deploys the file system by initializing it and returning a SecureFileHandler instance.