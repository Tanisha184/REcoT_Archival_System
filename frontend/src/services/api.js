import axios from 'axios';

const API_URL = 'http://localhost:5000';

// Authentication
export const loginUser = async (email, password) => {
  console.log('Attempting to log in with:', email);
  try {
    const response = await axios.post(`${API_URL}/api/auth/login`, { email, password });
    if (response.data.success) {
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Task Management
export const createTask = async (taskData) => {
  try {
    const response = await axios.post(`${API_URL}/api/tasks`, taskData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Query Management
export const searchTasks = async (filters) => {
  try {
    const response = await axios.post(`${API_URL}/api/tasks/search`, filters);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Archive Management
export const archiveTask = async (taskId) => {
  try {
    const response = await axios.post(`${API_URL}/api/tasks/archive/${taskId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const searchArchives = async (filters) => {
  try {
    const response = await axios.post(`${API_URL}/api/archives/search`, filters);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Report Management
export const getReportTemplates = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/report-templates`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const generateReport = async (templateName, filters) => {
  try {
    const response = await axios.post(`${API_URL}/api/reports/generate`, {
      template_name: templateName,
      filters
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Department Management
export const getDepartments = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/departments`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
