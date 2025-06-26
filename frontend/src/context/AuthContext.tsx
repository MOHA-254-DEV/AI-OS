import React, { createContext, useState, useEffect, useContext } from "react";
import { User } from "../types/user";
import { loginAPI, logoutAPI, getCurrentUserAPI } from "../api/auth";

interface AuthContextProps {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCurrentUserAPI()
      .then(setUser)
      .finally(() => setLoading(false));
  }, []);

  const login = async (username: string, password: string) => {
    setLoading(true);
    const userData = await loginAPI(username, password);
    setUser(userData);
    setLoading(false);
  };

  const logout = async () => {
    setLoading(true);
    await logoutAPI();
    setUser(null);
    setLoading(false);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
