import axios from "axios";
import { API_BASE } from "../utils/config";
import { User, AuthToken } from "../types/user";

// User login
export async function loginAPI(username: string, password: string): Promise<User> {
  const res = await axios.post(`${API_BASE}/auth/login`, { username, password });
  if (res.data && res.data.token) {
    localStorage.setItem("token", res.data.token);
  }
  return res.data.user;
}

// User logout
export async function logoutAPI(): Promise<void> {
  localStorage.removeItem("token");
  await axios.post(`${API_BASE}/auth/logout`);
}

// Get current user from backend (requires token)
export async function getCurrentUserAPI(): Promise<User | null> {
  const token = localStorage.getItem("token");
  if (!token) return null;
  try {
    const res = await axios.get(`${API_BASE}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return res.data.user;
  } catch {
    return null;
  }
}
