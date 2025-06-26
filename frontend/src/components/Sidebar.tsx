import React from "react";
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Tooltip,
  Divider,
  Box,
} from "@mui/material";
import ComputerIcon from "@mui/icons-material/Computer";
import FolderIcon from "@mui/icons-material/Folder";
import SettingsIcon from "@mui/icons-material/Settings";
import SearchIcon from "@mui/icons-material/Search";
import PeopleIcon from "@mui/icons-material/People";
import WifiIcon from "@mui/icons-material/Wifi";
import TerminalIcon from "@mui/icons-material/Terminal";
import { useNavigate } from "react-router-dom";

const icons = [
  <ComputerIcon />,
  <FolderIcon />,
  <SettingsIcon />,
  <SearchIcon />,
  <PeopleIcon />,
  <WifiIcon />,
  <TerminalIcon />,
];

const paths = [
  "/",
  "/files",
  "/settings",
  "/search",
  "/users",
  "/network",
  "/terminal"
];

const colors = [
  "#1976d2",
  "#388e3c",
  "#ffb300",
  "#d32f2f",
  "#8e24aa",
  "#0097a7",
  "#c62828",
];

function Sidebar({
  selectedTab,
  setSelectedTab,
  tabNames,
}: {
  selectedTab: number;
  setSelectedTab: (n: number) => void;
  tabNames: string[];
}) {
  const navigate = useNavigate();
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 90,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {
          width: 90,
          boxSizing: "border-box",
          background: "#f5f5f5",
          borderRight: "1px solid #e0e0e0",
        },
      }}
    >
      <ToolbarSpacer />
      <Divider />
      <List>
        {tabNames.map((tab, idx) => (
          <Tooltip title={tab} placement="right" key={tab}>
            <ListItem disablePadding>
              <ListItemButton
                selected={selectedTab === idx}
                onClick={() => {
                  setSelectedTab(idx);
                  navigate(paths[idx]);
                }}
                sx={{
                  my: 1,
                  borderRadius: 3,
                  background: selectedTab === idx ? colors[idx] : "none",
                  "&:hover": {
                    background: selectedTab === idx
                      ? colors[idx]
                      : `${colors[idx]}22`,
                  },
                  color: selectedTab === idx ? "#fff" : colors[idx],
                  boxShadow:
                    selectedTab === idx
                      ? "0 2px 6px 1px rgba(20,20,40,0.12)"
                      : "none",
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    color: selectedTab === idx ? "#fff" : colors[idx],
                    justifyContent: "center",
                  }}
                >
                  {icons[idx]}
                </ListItemIcon>
                <ListItemText
                  primary={tab}
                  sx={{
                    display: { xs: "none", md: "block" },
                    ml: 2,
                    color: selectedTab === idx ? "#fff" : colors[idx],
                  }}
                />
              </ListItemButton>
            </ListItem>
          </Tooltip>
        ))}
      </List>
      <Divider />
      <Box sx={{ flexGrow: 1 }} />
    </Drawer>
  );
}
function ToolbarSpacer() {
  return <Box sx={{ height: 64 }} />;
}
export default Sidebar;
