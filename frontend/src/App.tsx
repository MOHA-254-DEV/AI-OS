import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { NotificationProvider } from "./context/NotificationContext";
import { OrganizationProvider } from "./context/OrganizationContext";
import LoginForm from "./components/Auth/LoginForm";
import RegisterForm from "./components/Auth/RegisterForm";
import ForgotPassword from "./components/Auth/ForgotPassword";
import ResetPassword from "./components/Auth/ResetPassword";
import Dashboard from "./components/Dashboard/Overview";
import Notifications from "./components/Dashboard/Notifications";
import Organizations from "./components/Dashboard/Organizations";
import Files from "./components/Dashboard/Files";
import Network from "./components/Dashboard/Network";
import Firewall from "./components/Dashboard/Firewall";
import Quota from "./components/Dashboard/Quota";
import Users from "./components/Dashboard/Users";
import Header from "./components/Layout/Header";
import Sidebar from "./components/Layout/Sidebar";
import ProtectedRoute from "./components/Common/ProtectedRoute";

const App = () => (
  <AuthProvider>
    <NotificationProvider>
      <OrganizationProvider>
        <BrowserRouter>
          <Header />
          <Sidebar />
          <main style={{ padding: "1rem", marginLeft: 250 }}>
            <Routes>
              <Route path="/login" element={<LoginForm />} />
              <Route path="/register" element={<RegisterForm />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/reset-password/:token" element={<ResetPassword />} />
              <Route
                path="/"
                element={<ProtectedRoute><Dashboard /></ProtectedRoute>}
              />
              <Route
                path="/notifications"
                element={<ProtectedRoute><Notifications /></ProtectedRoute>}
              />
              <Route
                path="/organizations"
                element={<ProtectedRoute><Organizations /></ProtectedRoute>}
              />
              <Route
                path="/files"
                element={<ProtectedRoute><Files /></ProtectedRoute>}
              />
              <Route
                path="/network"
                element={<ProtectedRoute><Network /></ProtectedRoute>}
              />
              <Route
                path="/firewall"
                element={<ProtectedRoute><Firewall /></ProtectedRoute>}
              />
              <Route
                path="/quota"
                element={<ProtectedRoute><Quota /></ProtectedRoute>}
              />
              <Route
                path="/users"
                element={<ProtectedRoute><Users /></ProtectedRoute>}
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </BrowserRouter>
      </OrganizationProvider>
    </NotificationProvider>
  </AuthProvider>
);

export default App;
