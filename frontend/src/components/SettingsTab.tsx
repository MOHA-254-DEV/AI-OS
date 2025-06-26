import React, { useState } from "react";
import {
  Box,
  Typography,
  Tabs,
  Tab,
  Switch,
  FormControlLabel,
  Divider,
  Paper,
  Grid,
  Button,
  TextField,
  Snackbar,
  Alert,
  List,
  ListItem,
  ListItemText,
  Select,
  MenuItem,
  Avatar,
  InputLabel,
  FormControl,
  Chip,
  CircularProgress,
} from "@mui/material";
import { useAuth } from "../context/AuthContext";
import { useOS } from "../context/OSContext";
import { APP_NAME, APP_VERSION, FEATURE_FLAGS } from "../utils/config";
import { isValidEmail, isStrongPassword } from "../utils/validators";

function a11yProps(index: number) {
  return { id: `settings-tab-${index}`, "aria-controls": `settings-tabpanel-${index}` };
}

const themes = ["Default", "Oceanic", "Solarized", "Dark", "Light"];

export default function SettingsTab({
  darkMode,
  setDarkMode,
}: {
  darkMode: boolean;
  setDarkMode: (n: boolean) => void;
}) {
  const [tab, setTab] = useState(0);
  const [saved, setSaved] = useState(false);
  const { user } = useAuth();
  const { addNotification } = useOS();

  const [profile, setProfile] = useState({
    name: user?.name || "",
    email: user?.email || "",
    bio: "",
    avatar: user?.avatarUrl || "",
  });

  const [password, setPassword] = useState("");
  const [repeatPass, setRepeatPass] = useState("");
  const [passError, setPassError] = useState("");
  const [theme, setTheme] = useState(themes[0]);
  const [loading, setLoading] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) =>
    setProfile({ ...profile, [e.target.name]: e.target.value });

  const handleSaveProfile = () => {
    if (!isValidEmail(profile.email)) {
      addNotification("Invalid email format.");
      return;
    }
    setSaved(true);
    addNotification("Profile updated.");
  };

  const handleChangePass = () => {
    setPassError("");
    if (!isStrongPassword(password)) {
      setPassError("Password must be at least 8 characters, contain uppercase, lowercase and a number.");
      return;
    }
    if (password !== repeatPass) {
      setPassError("Passwords do not match.");
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setPassword("");
      setRepeatPass("");
      setPassError("");
      setSaved(true);
      addNotification("Password changed.");
    }, 1200);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>
      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 2 }}>
        <Tab label="Profile" {...a11yProps(0)} />
        <Tab label="Preferences" {...a11yProps(1)} />
        <Tab label="Security" {...a11yProps(2)} />
        <Tab label="Advanced" {...a11yProps(3)} />
        <Tab label="About" {...a11yProps(4)} />
      </Tabs>
      {tab === 0 && (
        <Paper sx={{ p: 3, maxWidth: 600 }}>
          <Typography variant="h6" mb={2}>
            Edit Profile
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Avatar src={profile.avatar} sx={{ width: 56, height: 56, mb: 2 }} />
              <TextField
                label="Name"
                name="name"
                value={profile.name}
                onChange={handleChange}
                fullWidth
                sx={{ my: 1 }}
              />
              <TextField
                label="Email"
                name="email"
                value={profile.email}
                onChange={handleChange}
                fullWidth
                sx={{ my: 1 }}
              />
              <TextField
                label="Bio"
                name="bio"
                value={profile.bio}
                onChange={handleChange}
                fullWidth
                multiline
                minRows={3}
                sx={{ my: 1 }}
              />
            </Grid>
          </Grid>
          <Divider sx={{ my: 2 }} />
          <Button
            variant="contained"
            onClick={handleSaveProfile}
            sx={{ mt: 2 }}
          >
            Save Profile
          </Button>
        </Paper>
      )}
      {tab === 1 && (
        <Paper sx={{ p: 3, maxWidth: 600 }}>
          <Typography variant="h6" mb={2}>
            Preferences
          </Typography>
          <FormControlLabel
            control={
              <Switch
                checked={darkMode}
                onChange={() => setDarkMode(!darkMode)}
              />
            }
            label="Dark Mode"
            sx={{ display: FEATURE_FLAGS.enableDarkMode ? "flex" : "none" }}
          />
          <Divider sx={{ my: 2 }} />
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel id="theme-label">Theme</InputLabel>
            <Select
              labelId="theme-label"
              value={theme}
              label="Theme"
              onChange={(e) => setTheme(e.target.value)}
            >
              {themes.map((th) => (
                <MenuItem value={th} key={th}>
                  {th}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControlLabel control={<Switch />} label="Enable Notifications" />
          <FormControlLabel control={<Switch />} label="Auto Update" />
          <Divider sx={{ my: 2 }} />
          <Chip label="Preferences saved automatically" color="info" />
        </Paper>
      )}
      {tab === 2 && (
        <Paper sx={{ p: 3, maxWidth: 600 }}>
          <Typography variant="h6" mb={2}>
            Security Settings
          </Typography>
          <TextField
            label="New Password"
            type="password"
            fullWidth
            sx={{ my: 1 }}
            value={password}
            onChange={e => setPassword(e.target.value)}
          />
          <TextField
            label="Repeat Password"
            type="password"
            fullWidth
            sx={{ my: 1 }}
            value={repeatPass}
            onChange={e => setRepeatPass(e.target.value)}
          />
          <Button
            variant="contained"
            color="secondary"
            onClick={handleChangePass}
            disabled={loading}
            sx={{ mt: 2 }}
          >
            {loading ? <CircularProgress size={18} /> : "Change Password"}
          </Button>
          {passError && (
            <Alert severity="error" sx={{ mt: 2 }}>{passError}</Alert>
          )}
        </Paper>
      )}
      {tab === 3 && (
        <Paper sx={{ p: 3, maxWidth: 600 }}>
          <Typography variant="h6" mb={2}>
            Advanced Settings
          </Typography>
          <List>
            <ListItem>
              <ListItemText
                primary="Reset Settings"
                secondary="Restore all settings to default values."
              />
              <Button variant="outlined" color="warning">
                Reset
              </Button>
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Export Configuration"
                secondary="Download your settings as a config file."
              />
              <Button variant="outlined">Export</Button>
            </ListItem>
          </List>
        </Paper>
      )}
      {tab === 4 && (
        <Paper sx={{ p: 3, maxWidth: 600 }}>
          <Typography variant="h6" mb={2}>
            About {APP_NAME}
          </Typography>
          <Typography>
            Version {APP_VERSION} <br />
            <b>{APP_NAME}</b> is an open-source, intelligent operating system UI built
            for AI agent workflow and human collaboration.<br />
            &copy; 2025 MOHA-254-DEV. All rights reserved.
          </Typography>
          <Divider sx={{ my: 2 }} />
          <Button
            variant="contained"
            href="https://github.com/MOHA-254-DEV/AI-OS"
            target="_blank"
          >
            GitHub Repo
          </Button>
        </Paper>
      )}
      <Snackbar
        open={saved}
        autoHideDuration={2000}
        onClose={() => setSaved(false)}
      >
        <Alert severity="success" sx={{ width: "100%" }}>
          Profile/settings saved!
        </Alert>
      </Snackbar>
    </Box>
  );
}
