import React, { createContext, useState, useEffect, useContext, ReactNode } from "react";
import { User } from "../types/user";
import * as authApi from "../api/auth";

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  register: (username: string, password: string, email: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem("aios_token"));

  useEffect(() => {
    if (token) {
      authApi.me(token).then(setUser).catch(() => logout());
    }
  }, [token]);

  const login = async (username: string, password: string) => {
    const { access_token } = await authApi.login(username, password);
    setToken(access_token);
    localStorage.setItem("aios_token", access_token);
    const me = await authApi.me(access_token);
    setUser(me);
  };

  const register = async (username: string, password: string, email: string) => {
    await authApi.register(username, password, email);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("aios_token");
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
