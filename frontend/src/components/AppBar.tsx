import React, { useState } from "react";
import {
  AppBar as MuiAppBar,
  Toolbar,
  Typography,
  IconButton,
  Avatar,
  Tooltip,
  Menu,
  MenuItem,
  InputBase,
  Box,
  Badge,
  Switch,
  Divider,
  ListItemIcon,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import SearchIcon from "@mui/icons-material/Search";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import NotificationsIcon from "@mui/icons-material/Notifications";
import SettingsIcon from "@mui/icons-material/Settings";
import PersonIcon from "@mui/icons-material/Person";
import LogoutIcon from "@mui/icons-material/Logout";
import { alpha, styled } from "@mui/material/styles";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useOS } from "../context/OSContext";
import { APP_NAME } from "../utils/config";

const Search = styled("div")(({ theme }) => ({
  position: "relative",
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.20),
  "&:hover": { backgroundColor: alpha(theme.palette.common.white, 0.35) },
  marginRight: theme.spacing(2),
  marginLeft: 0,
  width: "100%",
  [theme.breakpoints.up("sm")]: { marginLeft: theme.spacing(3), width: "auto" },
}));
const SearchIconWrapper = styled("div")(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: "100%",
  position: "absolute",
  pointerEvents: "none",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
}));
const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: "inherit",
  "& .MuiInputBase-input": {
    padding: theme.spacing(1, 1, 1, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create("width"),
    width: "100%",
    [theme.breakpoints.up("md")]: { width: "20ch" },
  },
}));

const notificationMock = [
  { id: 1, message: "System update available", type: "info" },
  { id: 2, message: "New user login: ai-agent", type: "success" },
  { id: 3, message: "File 'plan.docx' uploaded", type: "info" },
];

const userMenuItems = [
  { label: "Profile", icon: <PersonIcon fontSize="small" />, path: "/users" },
  { label: "Settings", icon: <SettingsIcon fontSize="small" />, path: "/settings" },
];

function AppBar({
  selectedTab,
  setSelectedTab,
  darkMode,
  setDarkMode,
  tabNames,
}: {
  selectedTab: number;
  setSelectedTab: (n: number) => void;
  darkMode: boolean;
  setDarkMode: (n: boolean) => void;
  tabNames: string[];
}) {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [notifAnchorEl, setNotifAnchorEl] = useState<null | HTMLElement>(null);
  const [searchText, setSearchText] = useState("");
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { notifications } = useOS();

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => setAnchorEl(event.currentTarget);
  const handleClose = () => setAnchorEl(null);

  const handleNotifMenu = (event: React.MouseEvent<HTMLElement>) => setNotifAnchorEl(event.currentTarget);
  const handleNotifClose = () => setNotifAnchorEl(null);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setSelectedTab(tabNames.indexOf("Search"));
    navigate("/search");
  };

  const handleUserItem = (path: string) => {
    navigate(path);
    handleClose();
  };

  return (
    <MuiAppBar position="sticky" color="primary" sx={{ zIndex: 1201 }}>
      <Toolbar>
        <IconButton size="large" edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" noWrap component="div">
          {APP_NAME}
        </Typography>
        <Box sx={{ flexGrow: 1 }} />
        <form onSubmit={handleSearch}>
          <Search>
            <SearchIconWrapper>
              <SearchIcon />
            </SearchIconWrapper>
            <StyledInputBase
              placeholder={`Search…`}
              inputProps={{ "aria-label": "search" }}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              onFocus={() => {
                setSelectedTab(tabNames.indexOf("Search"));
                navigate("/search");
              }}
            />
          </Search>
        </form>
        <Tooltip title={darkMode ? "Light mode" : "Dark mode"}>
          <Switch
            checked={darkMode}
            onChange={() => setDarkMode(!darkMode)}
            icon={<Brightness7Icon />}
            checkedIcon={<Brightness4Icon />}
            color="default"
          />
        </Tooltip>
        <IconButton color="inherit" onClick={handleNotifMenu}>
          <Badge badgeContent={notifications.length || notificationMock.length} color="error">
            <NotificationsIcon />
          </Badge>
        </IconButton>
        <Menu
          anchorEl={notifAnchorEl}
          open={Boolean(notifAnchorEl)}
          onClose={handleNotifClose}
          PaperProps={{ style: { minWidth: 260 } }}
        >
          {[...notifications, ...notificationMock].slice(0, 5).map((notif: any, idx) => (
            <MenuItem key={idx} dense>
              <Typography variant="body2" color={notif.type === "error" ? "error" : "primary"}>
                {notif.message || notif}
              </Typography>
            </MenuItem>
          ))}
          <Divider />
          <MenuItem onClick={handleNotifClose}>View all notifications</MenuItem>
        </Menu>
        <IconButton color="inherit" onClick={handleMenu}>
          <Avatar sx={{ bgcolor: "#1976d2" }} src={user?.avatarUrl}>
            <PersonIcon />
          </Avatar>
        </IconButton>
        <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleClose}>
          {userMenuItems.map((item) => (
            <MenuItem key={item.label} onClick={() => handleUserItem(item.path)}>
              <ListItemIcon>{item.icon}</ListItemIcon>
              {item.label}
            </MenuItem>
          ))}
          <Divider />
          <MenuItem
            onClick={() => {
              logout();
              handleClose();
            }}
          >
            <ListItemIcon>
              <LogoutIcon fontSize="small" />
            </ListItemIcon>
            Logout
          </MenuItem>
        </Menu>
      </Toolbar>
    </MuiAppBar>
  );
}

export default AppBar;
