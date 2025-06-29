import api from "../utils/apiClient";
import { User } from "../types/user";

export async function login(username: string, password: string): Promise<{ access_token: string }> {
  const res = await api.post("/auth/login", { username, password });
  return res.data;
}

export async function register(username: string, password: string, email: string): Promise<void> {
  await api.post("/auth/register", { username, password, email });
}

export async function me(token: string): Promise<User> {
  const res = await api.get("/users/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}
