#define SECURESTORAGE_EXPORTS

#include "SecureStorage.h"
#include <string>
#include <unordered_map>
#include <vector>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <memory>

class SecureStorage {
public:
    SecureStorage(const std::string& base_path) : base_path(base_path) {
        index_file = base_path + "/index.json";
        load_index();
    }

    ~SecureStorage() {
        save_index();
    }

    bool add_file(const std::string& file_path, const std::string& encrypted_path) {
        std::vector<std::string> parts = split(file_path, '/');
        DirectoryEntry& parent = navigate_to_directory(std::vector<std::string>(parts.begin(), parts.end() - 1));
        parent.contents[parts.back()] = {"file", {}, encrypted_path};
        save_index();
        return true;
    }

    std::string get_file_path(const std::string& file_path) {
        std::vector<std::string> parts = split(file_path, '/');
        DirectoryEntry& parent = navigate_to_directory(std::vector<std::string>(parts.begin(), parts.end() - 1));
        auto it = parent.contents.find(parts.back());
        if (it != parent.contents.end() && it->second.type == "file") {
            return it->second.path;
        }
        return "";
    }

    bool remove_file(const std::string& file_path) {
        std::vector<std::string> parts = split(file_path, '/');
        DirectoryEntry& parent = navigate_to_directory(std::vector<std::string>(parts.begin(), parts.end() - 1));
        auto it = parent.contents.find(parts.back());
        if (it != parent.contents.end() && it->second.type == "file") {
            parent.contents.erase(it);
            save_index();
            return true;
        }
        return false;
    }

    std::string get_file_structure() {
        return serialize_directory(root);
    }

    bool create_directory(const std::string& dir_path) {
        std::vector<std::string> parts = split(dir_path, '/');
        DirectoryEntry& parent = navigate_to_directory(parts);
        save_index();
        return true;
    }

    bool rename_directory(const std::string& old_path, const std::string& new_path) {
        std::vector<std::string> old_parts = split(old_path, '/');
        std::vector<std::string> new_parts = split(new_path, '/');
        DirectoryEntry& old_parent = navigate_to_directory(std::vector<std::string>(old_parts.begin(), old_parts.end() - 1));
        DirectoryEntry& new_parent = navigate_to_directory(std::vector<std::string>(new_parts.begin(), new_parts.end() - 1));
        auto it = old_parent.contents.find(old_parts.back());
        if (it != old_parent.contents.end() && it->second.type == "directory") {
            new_parent.contents[new_parts.back()] = std::move(it->second);
            old_parent.contents.erase(it);
            save_index();
            return true;
        }
        return false;
    }

    bool delete_directory(const std::string& dir_path) {
        std::vector<std::string> parts = split(dir_path, '/');
        DirectoryEntry& parent = navigate_to_directory(std::vector<std::string>(parts.begin(), parts.end() - 1));
        auto it = parent.contents.find(parts.back());
        if (it != parent.contents.end() && it->second.type == "directory") {
            parent.contents.erase(it);
            save_index();
            return true;
        }
        return false;
    }

    bool move_file(const std::string& src_path, const std::string& dest_path) {
        std::vector<std::string> src_parts = split(src_path, '/');
        std::vector<std::string> dest_parts = split(dest_path, '/');
        DirectoryEntry& src_parent = navigate_to_directory(std::vector<std::string>(src_parts.begin(), src_parts.end() - 1));
        DirectoryEntry& dest_parent = navigate_to_directory(std::vector<std::string>(dest_parts.begin(), dest_parts.end() - 1));
        auto it = src_parent.contents.find(src_parts.back());
        if (it != src_parent.contents.end() && it->second.type == "file") {
            dest_parent.contents[dest_parts.back()] = std::move(it->second);
            src_parent.contents.erase(it);
            save_index();
            return true;
        }
        return false;
    }

    bool directory_exists(const std::string& dir_path) {
        try {
            std::vector<std::string> parts = split(dir_path, '/');
            DirectoryEntry& dir = navigate_to_directory(parts);
            return dir.type == "directory";
        } catch (const std::runtime_error&) {
            return false;
        }
    }

private:
    struct DirectoryEntry {
        std::string type;
        std::unordered_map<std::string, DirectoryEntry> contents;
        std::string path;
    };

    std::string base_path;
    std::string index_file;
    DirectoryEntry root;

    void load_index() {
        std::ifstream file(index_file);
        if (file) {
            root = deserialize_directory(file);
        } else {
            root = {"directory", {}, ""};
        }
    }

    void save_index() {
        std::ofstream file(index_file);
        serialize_directory(root, file);
    }

    DirectoryEntry& navigate_to_directory(const std::vector<std::string>& parts) {
        DirectoryEntry* current = &root;
        for (const auto& part : parts) {
            if (part.empty()) continue;
            auto it = current->contents.find(part);
            if (it == current->contents.end()) {
                it = current->contents.insert({part, {"directory", {}, ""}}).first;
            }
            if (it->second.type != "directory") {
                throw std::runtime_error("Invalid path");
            }
            current = &it->second;
        }
        return *current;
    }

    static std::vector<std::string> split(const std::string& s, char delimiter) {
        std::vector<std::string> tokens;
        std::string token;
        std::istringstream tokenStream(s);
        while (std::getline(tokenStream, token, delimiter)) {
            tokens.push_back(token);
        }
        return tokens;
    }

    static void serialize_directory(const DirectoryEntry& entry, std::ostream& os, int indent = 0) {
        os << std::string(indent, ' ') << "{\n";
        os << std::string(indent + 2, ' ') << "\"type\": \"" << entry.type << "\",\n";
        if (!entry.path.empty()) {
            os << std::string(indent + 2, ' ') << "\"path\": \"" << entry.path << "\",\n";
        }
        os << std::string(indent + 2, ' ') << "\"contents\": {\n";
        for (const auto& [name, subentry] : entry.contents) {
            os << std::string(indent + 4, ' ') << "\"" << name << "\": ";
            serialize_directory(subentry, os, indent + 4);
            os << ",\n";
        }
        os << std::string(indent + 2, ' ') << "}\n";
        os << std::string(indent, ' ') << "}";
    }

    static std::string serialize_directory(const DirectoryEntry& entry) {
        std::ostringstream oss;
        serialize_directory(entry, oss);
        return oss.str();
    }

    static DirectoryEntry deserialize_directory(std::istream& is) {
        return {"directory", {}, ""};
    }
};

extern "C" {
    SECURESTORAGE_API void* CreateSecureStorage(const char* base_path) {
        return new SecureStorage(base_path);
    }

    SECURESTORAGE_API void DestroySecureStorage(void* storage) {
        delete static_cast<SecureStorage*>(storage);
    }

    SECURESTORAGE_API int AddFile(void* storage, const char* file_path, const char* encrypted_path) {
        return static_cast<SecureStorage*>(storage)->add_file(file_path, encrypted_path);
    }

    SECURESTORAGE_API const char* GetFilePath(void* storage, const char* file_path) {
        static std::string result;
        result = static_cast<SecureStorage*>(storage)->get_file_path(file_path);
        return result.c_str();
    }

    SECURESTORAGE_API int RemoveFile(void* storage, const char* file_path) {
        return static_cast<SecureStorage*>(storage)->remove_file(file_path);
    }

    SECURESTORAGE_API const char* GetFileStructure(void* storage) {
        static std::string result;
        result = static_cast<SecureStorage*>(storage)->get_file_structure();
        return result.c_str();
    }

    SECURESTORAGE_API int CreateDirectory(void* storage, const char* dir_path) {
        return static_cast<SecureStorage*>(storage)->create_directory(dir_path);
    }

    SECURESTORAGE_API int RenameDirectory(void* storage, const char* old_path, const char* new_path) {
        return static_cast<SecureStorage*>(storage)->rename_directory(old_path, new_path);
    }

    SECURESTORAGE_API int DeleteDirectory(void* storage, const char* dir_path) {
        return static_cast<SecureStorage*>(storage)->delete_directory(dir_path);
    }

    SECURESTORAGE_API int MoveFile(void* storage, const char* src_path, const char* dest_path) {
        return static_cast<SecureStorage*>(storage)->move_file(src_path, dest_path);
    }

    SECURESTORAGE_API int DirectoryExists(void* storage, const char* dir_path) {
        return static_cast<SecureStorage*>(storage)->directory_exists(dir_path);
    }
}