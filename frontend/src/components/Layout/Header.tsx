import React from "react";
import { useAuth } from "../../context/AuthContext";

const Header: React.FC = () => {
  const { user, logout } = useAuth();
  return (
    <header style={{ background: "#292f36", color: "#fff", padding: "1rem", marginLeft: 220 }}>
      <span style={{ fontWeight: "bold", fontSize: "1.3rem" }}>AI-OS Dashboard</span>
      <span style={{ float: "right" }}>
        {user && (
          <>
            <span>{user.username}</span>
            <button style={{ marginLeft: 12 }} onClick={logout}>
              Logout
            </button>
          </>
        )}
      </span>
    </header>
  );
};
export default Header;
