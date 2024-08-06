#pragma once

#ifdef SECURESTORAGE_EXPORTS
#define SECURESTORAGE_API __declspec(dllexport)
#else
#define SECURESTORAGE_API __declspec(dllimport)
#endif

extern "C" {
    SECURESTORAGE_API void* CreateSecureStorage(const char* base_path);
    SECURESTORAGE_API void DestroySecureStorage(void* storage);
    SECURESTORAGE_API int AddFile(void* storage, const char* file_path, const char* encrypted_path);
    SECURESTORAGE_API const char* GetFilePath(void* storage, const char* file_path);
    SECURESTORAGE_API int RemoveFile(void* storage, const char* file_path);
    SECURESTORAGE_API const char* GetFileStructure(void* storage);
    SECURESTORAGE_API int CreateDirectory(void* storage, const char* dir_path);
    SECURESTORAGE_API int RenameDirectory(void* storage, const char* old_path, const char* new_path);
    SECURESTORAGE_API int DeleteDirectory(void* storage, const char* dir_path);
    SECURESTORAGE_API int MoveFile(void* storage, const char* src_path, const char* dest_path);
    SECURESTORAGE_API int DirectoryExists(void* storage, const char* dir_path);
}