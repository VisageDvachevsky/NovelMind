import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const deployFileSystem = async (basePath, masterPassword) => {
  const response = await axios.post(`${API_BASE_URL}/system/deploy`, {
    base_path: basePath,
    master_password: masterPassword,
  });
  return response.data;
};
