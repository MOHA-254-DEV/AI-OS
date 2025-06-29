
import axios from "axios";
import { API_BASE } from "../utils/config";
import { User } from "../types/user";

// List users
export async function listUsers(): Promise<User[]> {
  const token = localStorage.getItem("token");
  const res = await axios.get(`${API_BASE}/users`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data.users;
}

// Add new user
export async function addUser(user: Partial<User>): Promise<User> {
  const token = localStorage.getItem("token");
  const res = await axios.post(`${API_BASE}/users`, user, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data.user;
}

// Edit user
export async function editUser(id: string, data: Partial<User>): Promise<User> {
  const token = localStorage.getItem("token");
  const res = await axios.put(`${API_BASE}/users/${id}`, data, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data.user;
}

// Delete user
export async function deleteUser(id: string): Promise<void> {
  const token = localStorage.getItem("token");
  await axios.delete(`${API_BASE}/users/${id}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

