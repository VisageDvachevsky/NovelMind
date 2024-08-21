import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const addFile = async (filePath, fileId) => {
  const response = await axios.post(`${API_BASE_URL}/files/add_file`, {
    file_path: filePath,
    file_id: fileId,
  });
  return response.data;
};

export const readFile = async (fileId, decode = false) => {
  const response = await axios.get(`${API_BASE_URL}/files/read_file`, {
    params: { file_id: fileId, decode },
  });
  return response.data;
};

export const deleteFile = async (fileId) => {
  const response = await axios.delete(`${API_BASE_URL}/files/delete_file`, {
    params: { file_id: fileId },
  });
  return response.data;
};

export const listFiles = async () => {
  const response = await axios.get(`${API_BASE_URL}/files/list_files`);
  return response.data;
};

export const createDirectory = async (dirName) => {
  const response = await axios.post(`${API_BASE_URL}/files/create_directory`, {
    dir_name: dirName,
  });
  return response.data;
};

export const renameDirectory = async (oldName, newName) => {
  const response = await axios.put(`${API_BASE_URL}/files/rename_directory`, {
    old_name: oldName,
    new_name: newName,
  });
  return response.data;
};

export const deleteDirectory = async (dirName) => {
  const response = await axios.delete(`${API_BASE_URL}/files/delete_directory`, {
    params: { dir_name: dirName },
  });
  return response.data;
};

export const moveFile = async (fileId, destDir) => {
  const response = await axios.put(`${API_BASE_URL}/files/move_file`, {
    file_id: fileId,
    dest_dir: destDir,
  });
  return response.data;
};

export const changeDirectory = async (dirName) => {
  const response = await axios.put(`${API_BASE_URL}/files/change_directory`, {
    dir_name: dirName,
  });
  return response.data;
};

export const getCurrentDirectory = async () => {
  const response = await axios.get(`${API_BASE_URL}/files/current_directory`);
  return response.data;
};
