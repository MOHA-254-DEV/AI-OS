import React from "react";
import { Link } from "react-router-dom";

const Sidebar: React.FC = () => (
  <nav style={{
    width: 220,
    height: "100vh",
    position: "fixed",
    top: 0,
    left: 0,
    background: "#222",
    color: "#fff",
    padding: "1rem"
  }}>
    <ul style={{ listStyle: "none", padding: 0 }}>
      <li><Link to="/" style={{ color: "#fff" }}>Dashboard</Link></li>
      <li><Link to="/organizations" style={{ color: "#fff" }}>Organizations</Link></li>
      <li><Link to="/users" style={{ color: "#fff" }}>Users</Link></li>
      <li><Link to="/files" style={{ color: "#fff" }}>Files</Link></li>
      <li><Link to="/network" style={{ color: "#fff" }}>Network</Link></li>
      <li><Link to="/firewall" style={{ color: "#fff" }}>Firewall</Link></li>
      <li><Link to="/quota" style={{ color: "#fff" }}>Quota</Link></li>
      <li><Link to="/notifications" style={{ color: "#fff" }}>Notifications</Link></li>
    </ul>
  </nav>
);

export default Sidebar;
