import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const loginUser = async (email, password) => {
  console.log('Attempting to log in with:', email); // Log email for debugging
  try {
    const response = await axios.post(`${API_URL}/auth/login`, { email, password });
    return response.data;
  } catch (error) {
    console.error('Login error:', error);
    return { success: false, message: 'An error occurred. Please try again later.' };
  }
};

export const registerUser = async (formData) => {
  try {
    const response = await axios.post(`${API_URL}/auth/register`, formData);
    return response.data;
  } catch (error) {
    console.error('Registration error:', error);
    return { success: false, message: 'An error occurred. Please try again later.' };
  }
};

export const createTask = async (taskData) => {
  try {
    const response = await axios.post(`${API_URL}/tasks`, taskData);
    return response.data;
  } catch (error) {
    console.error('Error creating task:', error);
    return { success: false, message: 'An error occurred while creating the task.' };
  }
};

export const approveTask = async (taskId, approvalStatus) => {
  try {
    const response = await axios.post(`${API_URL}/tasks/approve/${taskId}`, { status: approvalStatus });
    return response.data;
  } catch (error) {
    console.error('Error approving task:', error);
    return { success: false, message: 'An error occurred while approving the task.' };
  }
};

export const manageUsers = async () => {
  try {
    const response = await axios.get(`${API_URL}/users`);
    return response.data;
  } catch (error) {
    console.error('Error managing users:', error);
    return [];
  }
};
