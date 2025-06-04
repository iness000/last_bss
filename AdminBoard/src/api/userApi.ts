import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api'; // Adjust if needed

export interface User {
  id: number;
  name: string;
  email: string;
  phone?: string;
  address?: string;
  license_number?: string;
  license_expiry?: string;
  motocycle_model?: string;
  motocycle_year?: string;
  subscription_plan_id?: number;
  subscription_start?: string;
  is_active: boolean;
  role: string;
  created_at: string;
  updated_at: string;
  status?: string;
  lastLogin?: string;
}

export interface CreateUserData {
  name: string;
  email: string;
  password_hash: string;
  phone?: string;
  address?: string;
  license_number?: string;
  license_expiry?: string;
  motocycle_model?: string;
  motocycle_year?: string;
  subscription_plan_id?: number;
  subscription_start?: string;
  is_active?: boolean;
  role?: string;
}

export interface UserData {
  name?: string;
  email?: string;
  role?: string;
  status?: string;
}

export const createUser = async (data: CreateUserData) => {
  const response = await axios.post(`${API_BASE_URL}/users`, data);
  return response.data;
};

export const updateUser = async (userId: number, data: UserData) =>
  axios.put(`${API_BASE_URL}/users/${userId}`, data);

export const deleteUser = async (userId: number) => {
  const response = await axios.delete(`${API_BASE_URL}/users/${userId}`);
  return response.data;
};

// working example
export const getUsers = async () => {
    const response =  await axios.get(`${API_BASE_URL}/users`);
    return response.data;
}
