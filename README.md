<div align="center">
  <img src="./Assets/logo.png" alt="NovelMind Logo" width="150" height="150">
  <h1>NovelMind</h1>
  <p><strong>Инновационный визуальный редактор для создания визуальных новелл</strong></p>
  <p>
    <img src="https://img.shields.io/badge/версия-0.0.1-blue.svg" alt="Версия">
    <img src="https://img.shields.io/badge/лицензия-MIT-green.svg" alt="Лицензия">
    <img src="https://img.shields.io/github/last-commit/VisageDvachevsky/NovelMind" alt="Активность">
  </p>
</div>

---

**NovelMind** - это проект, направленный на упрощение процесса создания визуальных новелл, предоставляя разработчикам мощные инструменты в удобном визуальном интерфейсе, одновременно обеспечивая безопасность их работы.


## 📑 Оглавление

- [Ключевые особенности](#-ключевые-особенности)
- [Файловая система](#-файловая-система)
- [Система логирования](#-система-логирования)

## 🌟 Ключевые особенности

1. 🔐 **Безопасная файловая система**: Встроенная система шифрования файлов предотвращает несанкционированный доступ к ресурсам проекта.

2. 🖱️ **Визуальное позиционирование элементов**: Интуитивно понятный интерфейс позволяет разработчикам перетаскивать спрайты и другие элементы непосредственно на сцену.

3. 🎭 **Визуальное программирование**: Возможность визуально программировать ход новеллы, включая порядок диалогов и другие элементы повествования.

4. 🔧 **Внутренний язык программирования**: Собственный скриптовый язык для более тонкой настройки и программирования сложных сценариев.

5. 🚀 **Компиляция в исполняемый файл**: По завершении разработки, весь проект (включая ресурсы, диалоги и скрипты) может быть скомпилирован в единый исполняемый файл одним нажатием кнопки.

6. 🎮 **Простота использования**: Готовая новелла запускается простым запуском скомпилированного файла.

---

## 📁 Файловая система

Файловая система NovelMind обеспечивает безопасное хранение и управление файлами с использованием шифрования. Ниже представлена документация по компонентам ядра (Core) и API файловой системы.

<details>
<summary><strong>Компоненты ядра (Core)</strong></summary>

### Компоненты ядра (Core)

Основные компоненты включают следующие модули:

1. [Шифрование](#шифрование)
2. [Обработчик файлов](#обработчик-файлов)
3. [Инициализатор файловой системы](#инициализатор-файловой-системы)
4. [Безопасное хранилище](#безопасное-хранилище)
5. [Вспомогательные функции](#вспомогательные-функции)

#### Шифрование

Файл: `encryption.py`

##### Класс: AdvancedEncryptor

Класс для обработки шифрования и дешифрования данных с использованием AES шифрования.

Методы:
- `__init__(self, key_file: str = 'master_key.key', salt_file: str = 'salt.key') -> None`
- `_load_or_generate_key(self, file_path: str) -> bytes`
- `_derive_key(self, password: str) -> bytes`
- `encrypt(self, data: bytes, password: str) -> bytes`
- `decrypt(self, encrypted_data: bytes, password: str) -> bytes`

#### Обработчик файлов

Файл: `file_handler.py`

##### Класс: SecureFileHandler

Класс для обработки безопасных файловых операций, таких как добавление, чтение, удаление и перечисление файлов.

Методы:
- `__init__(self, base_path: str, master_password: str) -> None`
- `add_file(self, file_path: str, file_id: str) -> None`
- `read_file(self, file_id: str, decode: bool = False) -> str`
- `delete_file(self, file_id: str) -> None`
- `list_files(self) -> List[str]`

#### Инициализатор файловой системы

Файл: `initializer.py`

##### Класс: FileSystemInitializer

Класс для инициализации файловой системы для безопасного хранения.

Методы:
- `__init__(self, base_path: str, master_password: str) -> None`
- `initialize(self) -> None`
- `_initialize_encryption(self) -> None`
- `_create_empty_index(self) -> None`

#### Безопасное хранилище

Файл: `storage.py`

##### Класс: SecureStorage

Класс для обработки безопасного хранения и извлечения метаданных файлов.

Методы:
- `__init__(self, base_path: str, master_password: str) -> None`
- `_load_index(self) -> Dict[str, str]`
- `_save_index(self) -> None`
- `add_file(self, file_id: str, encrypted_path: str) -> None`
- `get_file_path(self, file_id: str) -> Optional[str]`
- `remove_file(self, file_id: str) -> None`
- `list_files(self) -> List[str]`

#### Вспомогательные функции

Файл: `utils.py`

Функции:
- `create_directory_if_not_exists(path: str) -> None`
- `is_valid_path(path: str) -> bool`

</details>

<details>
<summary><strong>API компоненты</strong></summary>

### API компоненты

API компоненты предоставляют высокоуровневые операции для управления файлами и развертывания системы:

1. [Файловые операции](#файловые-операции)
2. [Системные операции](#системные-операции)

#### Файловые операции

Файл: `file_operations.py`

##### Класс: FileOperations

Класс для выполнения файловых операций, таких как добавление, чтение, удаление и перечисление файлов.

Методы:
- `__init__(self, file_handler: SecureFileHandler) -> None`
- `add_file(self, file_path: str, file_id: str) -> None`
- `read_file(self, file_id: str, decode: bool = False) -> str`
- `delete_file(self, file_id: str) -> None`
- `list_files(self) -> List[str]`

#### Системные операции

Файл: `system_operations.py`

##### Класс: SystemOperations

Класс для выполнения системных операций, таких как развертывание файловой системы.

Методы:
- `deploy(base_path: str, master_password: str) -> SecureFileHandler`

</details>

---

## 📊 Система логирования

Система логирования NovelMind предоставляет гибкие и многофункциональные возможности для ведения логов, обеспечивая поддержку многоуровневого логирования, форматирования в JSON и автоматического логирования функций и классов.

### Содержание

- [Основные функции](#основные-функции)
- [Класс Logger](#класс-logger)
- [Примеры использования](#примеры-использования)

### Основные функции

1. **Многоуровневое логирование**: Поддержка уровней DEBUG, INFO, WARNING, ERROR и CRITICAL.
2. **Логирование в файл и консоль**: Логи записываются в файл с возможностью ограничения размера и ротации файлов.
3. **Форматирование в JSON**: Возможность форматирования логов в JSON для упрощения анализа и парсинга.
4. **Автоматическое логирование функций**: Декоратор для автоматического логирования вызовов функций, аргументов, возвращаемых значений и времени выполнения.
5. **Логирование классов**: Декоратор для автоматического применения логирования ко всем методам класса.
6. **Дополнительный контекст**: Возможность добавления дополнительной контекстной информации к сообщениям логов.
7. **Порог ошибок**: Ограничение количества одинаковых сообщений об ошибках в заданное время.
8. **Информация о системе**: Логирование текущей системной информации (ЦПУ, память, дисковая активность).
9. **Идентификатор трассировки**: Установка уникального идентификатора для трассировки логов.
10. **Профилирование функций**: Декоратор для профилирования выполнения функций и сохранения результатов.

### Класс Logger

#### Инициализация

```python
Logger(log_file: str = 'app.log', use_json: bool = False, 
       max_log_size: int = 10*1024*1024, backup_count: int = 5,
       error_threshold: int = 10, error_window: int = 3600)
```

- `log_file`: Имя файла для логов (по умолчанию: 'app.log')
- `use_json`: Булевый флаг для включения форматирования логов в JSON (по умолчанию: False)
- `max_log_size`: Максимальный размер файла лога в байтах перед ротацией (по умолчанию: 10 MB)
- `backup_count`: Количество резервных копий логов (по умолчанию: 5)
- `error_threshold`: Максимальное количество одинаковых сообщений об ошибках в заданное время (по умолчанию: 10)
- `error_window`: Временной интервал для подсчета ошибок в секундах (по умолчанию: 3600)

#### Методы

##### Методы логирования

- `debug(message: str, extra: Dict[str, Any] = None)`
- `info(message: str, extra: Dict[str, Any] = None)`
- `warning(message: str, extra: Dict[str, Any] = None)`
- `error(message: str, extra: Dict[str, Any] = None)`
- `critical(message: str, extra: Dict[str, Any] = None)`

##### Методы-декораторы

- `log_function() -> Callable[[Callable], Callable]`
- `log_class() -> Callable[[Type], Type]`

##### Вспомогательные методы

- `set_trace_id()`: Установка уникального идентификатора для трассировки логов.
- `log_system_info()`: Логирование текущей системной информации (ЦПУ, память, дисковая активность).
- `profile(output_file=None) -> Callable[[Callable], Callable]`: Декоратор для профилирования выполнения функций.
- `set_log_level(logger_name: str, level: str)`: Установка уровня логирования для указанного логгера.

##### Контекстный менеджер

- `log_block(block_name: str)`: Контекстный менеджер для логирования блока кода с замером времени выполнения.

### Примеры использования

#### Базовое логирование

```python
logger = Logger()
logger.info("Приложение запущено")
logger.error("Произошла ошибка", extra={"error_code": 500})
```

#### Логирование функций

```python
logger = Logger()

@logger.log_function()
def example_function(a, b):
    return a + b

result = example_function(3, 4)
```

#### Логирование классов

```python
logger = Logger()

@logger.log_class()
class ExampleClass:
    def method1(self):
        pass

    def method2(self, x):
        return x * 2

obj = ExampleClass()
obj.method1()
obj.method2(5)
```

#### Логирование в формате JSON

```python
json_logger = Logger(use_json=True)
json_logger.info("Это лог в формате JSON", extra={"user_id": 123})
```

#### Контекстный менеджер для логирования блока кода

```python
logger = Logger()

with logger.log_block("Critical section"):
    pass
```

#### Логирование системной информации

```python
logger = Logger()
logger.log_system_info()
```

#### Установка уникального идентификатора трассировки

```python
logger = Logger()
logger.set_trace_id()
logger.info("Сообщение с trace_id")
```

#### Профилирование функций

```python
logger = Logger()

@logger.profile()
def compute():
    pass

compute()
```

#### Установка уровня логирования

```python
logger = Logger()
logger.set_log_level('Logger', 'WARNING')
```

<p align="center">
  Создано с ❤️ командой NovelMind
</p>