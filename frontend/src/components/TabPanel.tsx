import React from "react";
import { Routes, Route } from "react-router-dom";
import SystemTab from "./SystemTab";
import FilesTab from "./FilesTab";
import SettingsTab from "./SettingsTab";
import SearchTab from "./SearchTab";
import UserTab from "./UserTab";
import NetworkTab from "./NetworkTab";
import TerminalTab from "./TerminalTab";

function TabPanel({
  selectedTab,
  darkMode,
  setDarkMode,
}: {
  selectedTab: number;
  darkMode: boolean;
  setDarkMode: (n: boolean) => void;
}) {
  // Render based on router path (for deep-linking/multi-tab support)
  return (
    <Routes>
      <Route path="/" element={<SystemTab />} />
      <Route path="/files" element={<FilesTab />} />
      <Route path="/settings" element={<SettingsTab darkMode={darkMode} setDarkMode={setDarkMode} />} />
      <Route path="/search" element={<SearchTab />} />
      <Route path="/users" element={<UserTab />} />
      <Route path="/network" element={<NetworkTab />} />
      <Route path="/terminal" element={<TerminalTab />} />
    </Routes>
  );
}

export default TabPanel;
