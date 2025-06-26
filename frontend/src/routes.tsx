import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import App from "./App";
import Loader from "./components/Loader";
import FilesTab from "./components/FilesTab";
import SystemTab from "./components/SystemTab";
import SettingsTab from "./components/SettingsTab";
import SearchTab from "./components/SearchTab";
import UserTab from "./components/UserTab";
import NetworkTab from "./components/NetworkTab";
import TerminalTab from "./components/TerminalTab";
import { useAuth } from "./context/AuthContext";

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) return <Loader />;
  if (!user) return <Navigate to="/login" />;
  return <>{children}</>;
};

const RoutesConfig: React.FC = () => (
  <Routes>
    <Route
      path="/"
      element={
        <ProtectedRoute>
          <App />
        </ProtectedRoute>
      }
    >
      <Route index element={<SystemTab />} />
      <Route path="files" element={<FilesTab />} />
      <Route path="settings" element={<SettingsTab darkMode={false} setDarkMode={() => {}} />} />
      <Route path="search" element={<SearchTab />} />
      <Route path="users" element={<UserTab />} />
      <Route path="network" element={<NetworkTab />} />
      <Route path="terminal" element={<TerminalTab />} />
    </Route>
    <Route path="/login" element={<div>Login Page (to implement)</div>} />
    <Route path="*" element={<div>404 Not Found</div>} />
  </Routes>
);

export default RoutesConfig;
