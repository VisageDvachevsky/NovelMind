# NovelEditor

NovelEditor - это ....

## Файловая система NovelEditor

Файловая система NovelEditor обеспечивает безопасное хранение и управление файлами с использованием шифрования.

### Содержание

- [Компоненты ядра (Core)](#компоненты-ядра-core)
- [API компоненты](#api-компоненты)

## Компоненты ядра (Core)

Основные компоненты включают следующие модули:

1. [Шифрование](#шифрование)
2. [Обработчик файлов](#обработчик-файлов)
3. [Инициализатор файловой системы](#инициализатор-файловой-системы)
4. [Безопасное хранилище](#безопасное-хранилище)
5. [Вспомогательные функции](#вспомогательные-функции)

### Шифрование

Файл: `encryption.py`

#### Класс: AdvancedEncryptor

Класс для обработки шифрования и дешифрования данных с использованием AES шифрования.

Методы:
- `__init__(self, key_file: str = 'master_key.key', salt_file: str = 'salt.key') -> None`
- `_load_or_generate_key(self, file_path: str) -> bytes`
- `_derive_key(self, password: str) -> bytes`
- `encrypt(self, data: bytes, password: str) -> bytes`
- `decrypt(self, encrypted_data: bytes, password: str) -> bytes`

### Обработчик файлов

Файл: `file_handler.py`

#### Класс: SecureFileHandler

Класс для обработки безопасных файловых операций, таких как добавление, чтение, удаление и перечисление файлов.

Методы:
- `__init__(self, base_path: str, master_password: str) -> None`
- `add_file(self, file_path: str, file_id: str) -> None`
- `read_file(self, file_id: str, decode: bool = False) -> str`
- `delete_file(self, file_id: str) -> None`
- `list_files(self) -> List[str]`

### Инициализатор файловой системы

Файл: `initializer.py`

#### Класс: FileSystemInitializer

Класс для инициализации файловой системы для безопасного хранения.

Методы:
- `__init__(self, base_path: str, master_password: str) -> None`
- `initialize(self) -> None`
- `_initialize_encryption(self) -> None`
- `_create_empty_index(self) -> None`

### Безопасное хранилище

Файл: `storage.py`

#### Класс: SecureStorage

Класс для обработки безопасного хранения и извлечения метаданных файлов.

Методы:
- `__init__(self, base_path: str, master_password: str) -> None`
- `_load_index(self) -> Dict[str, str]`
- `_save_index(self) -> None`
- `add_file(self, file_id: str, encrypted_path: str) -> None`
- `get_file_path(self, file_id: str) -> Optional[str]`
- `remove_file(self, file_id: str) -> None`
- `list_files(self) -> List[str]`

### Вспомогательные функции

Файл: `utils.py`

Функции:
- `create_directory_if_not_exists(path: str) -> None`
- `is_valid_path(path: str) -> bool`

## API компоненты

API компоненты предоставляют высокоуровневые операции для управления файлами и развертывания системы:

1. [Файловые операции](#файловые-операции)
2. [Системные операции](#системные-операции)

### Файловые операции

Файл: `file_operations.py`

#### Класс: FileOperations

Класс для выполнения файловых операций, таких как добавление, чтение, удаление и перечисление файлов.

Методы:
- `__init__(self, file_handler: SecureFileHandler) -> None`
- `add_file(self, file_path: str, file_id: str) -> None`
- `read_file(self, file_id: str, decode: bool = False) -> str`
- `delete_file(self, file_id: str) -> None`
- `list_files(self) -> List[str]`

### Системные операции

Файл: `system_operations.py`

#### Класс: SystemOperations

Класс для выполнения системных операций, таких как развертывание файловой системы.

Методы:
- `deploy(base_path: str, master_password: str) -> SecureFileHandler`
```

Эта версия README.md теперь ясно указывает, что описываемые компоненты относятся к файловой системе более крупного проекта NovelEditor. Структура документации осталась прежней, но контекст был обновлен.

Если вам нужны дальнейшие изменения или дополнения, пожалуйста, дайте мне знать.