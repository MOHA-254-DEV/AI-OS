import React from "react";

const Footer: React.FC = () => (
  <footer style={{ background: "#222", color: "#fff", textAlign: "center", padding: "1em", marginTop: 30 }}>
    &copy; {new Date().getFullYear()} AI-OS
  </footer>
);

export default Footer;
