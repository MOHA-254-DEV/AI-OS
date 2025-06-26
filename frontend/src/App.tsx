import React, { useState, useMemo } from "react";
import { ThemeProvider, CssBaseline, Box } from "@mui/material";
import theme from "./theme";
import AppBar from "./components/AppBar";
import Sidebar from "./components/Sidebar";
import TabPanel from "./components/TabPanel";
import "./styles/global.css";

const tabNames = [
  "System",
  "Files",
  "Settings",
  "Search",
  "Users",
  "Network",
  "Terminal",
];

function App() {
  const [selectedTab, setSelectedTab] = useState(0);
  const [darkMode, setDarkMode] = useState(false);

  const muiTheme = useMemo(() => theme(darkMode), [darkMode]);

  return (
    <ThemeProvider theme={muiTheme}>
      <CssBaseline />
      <AppBar
        selectedTab={selectedTab}
        setSelectedTab={setSelectedTab}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        tabNames={tabNames}
      />
      <Box sx={{ display: "flex", minHeight: "100vh" }}>
        <Sidebar
          selectedTab={selectedTab}
          setSelectedTab={setSelectedTab}
          tabNames={tabNames}
        />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            background:
              "linear-gradient(120deg, #e3f2fd 0%, #ffffff 80%, #fce4ec 100%)",
            minHeight: "100vh",
            overflow: "auto",
          }}
        >
          <TabPanel
            selectedTab={selectedTab}
            darkMode={darkMode}
            setDarkMode={setDarkMode}
          />
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
