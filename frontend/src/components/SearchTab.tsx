import React, { useState } from "react";
import {
  Box,
  Typography,
  TextField,
  Paper,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Avatar,
  Chip,
  Divider,
  Button,
  Tabs,
  Tab,
  CircularProgress,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import FolderIcon from "@mui/icons-material/Folder";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";
import PersonIcon from "@mui/icons-material/Person";
import WifiIcon from "@mui/icons-material/Wifi";
import TerminalIcon from "@mui/icons-material/Terminal";
import { blue, green, orange, purple } from "@mui/material/colors";
import { useAuth } from "../context/AuthContext";
import { useFiles } from "../hooks/useFiles";
import { useNetworkInterfaces } from "../hooks/useNetwork";
import { listUsers } from "../api/users";
import { FileEntry } from "../types/files";
import { User } from "../types/user";
import { NetworkInfo } from "../types/network";

type SearchResult =
  | (FileEntry & { type: "file" | "folder" })
  | (User & { type: "user" })
  | (NetworkInfo & { type: "network" })
  | { type: "terminal"; name: string; snippet?: string };

const searchCategories = [
  { label: "All", value: "all" },
  { label: "Files", value: "files" },
  { label: "Folders", value: "folders" },
  { label: "Users", value: "users" },
  { label: "Network", value: "network" },
  { label: "Terminal", value: "terminal" },
];

function SearchTab() {
  const { user } = useAuth();
  const [tab, setTab] = useState(0);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const { files } = useFiles("Home");
  const { interfaces } = useNetworkInterfaces();

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setLoading(true);
    setSearched(true);
    let found: SearchResult[] = [];

    // Files and folders
    if (["all", "files", "folders"].includes(searchCategories[tab].value)) {
      found = [
        ...found,
        ...files
          .filter(
            (f) =>
              f.name.toLowerCase().includes(query.toLowerCase()) &&
              ((searchCategories[tab].value === "files" && f.type === "file") ||
                (searchCategories[tab].value === "folders" && f.type === "folder") ||
                searchCategories[tab].value === "all")
          )
          .map((f) => ({ ...f, type: f.type })),
      ];
    }

    // Users
    if (["all", "users"].includes(searchCategories[tab].value)) {
      try {
        const users: User[] = await listUsers();
        found = [
          ...found,
          ...users.filter(
            (u) =>
              u.name.toLowerCase().includes(query.toLowerCase()) ||
              u.email?.toLowerCase().includes(query.toLowerCase())
          ).map((u) => ({ ...u, type: "user" as const })),
        ];
      } catch {}
    }

    // Network
    if (["all", "network"].includes(searchCategories[tab].value)) {
      found = [
        ...found,
        ...interfaces.filter((ni) =>
          (ni.interface ?? "")
            .toLowerCase()
            .includes(query.toLowerCase())
        ).map((ni) => ({ ...ni, type: "network" as const })),
      ];
    }

    // Terminal (history, commands)
    if (["all", "terminal"].includes(searchCategories[tab].value)) {
      if (
        ["help", "whoami", "time", "echo", "clear"].some((cmd) =>
          cmd.startsWith(query.toLowerCase())
        )
      ) {
        found.push({
          type: "terminal",
          name: "Terminal Command",
          snippet: `Command: ${query}`,
        });
      }
    }

    setTimeout(() => {
      setResults(found);
      setLoading(false);
    }, 500); // Simulate API/network delay
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Search
      </Typography>
      <Paper sx={{ p: 2, mb: 2 }}>
        <form onSubmit={handleSearch}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={5}>
              <TextField
                fullWidth
                placeholder="Search files, folders, users, network, terminal..."
                variant="outlined"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                InputProps={{
                  startAdornment: <SearchIcon sx={{ mr: 1 }} />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={5}>
              <Tabs
                value={tab}
                onChange={(_, v) => setTab(v)}
                textColor="primary"
                indicatorColor="primary"
                variant="scrollable"
                scrollButtons="auto"
                aria-label="search categories"
              >
                {searchCategories.map((cat) => (
                  <Tab key={cat.value} label={cat.label} />
                ))}
              </Tabs>
            </Grid>
            <Grid item xs={12} md={2}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                startIcon={<SearchIcon />}
                disabled={loading}
              >
                Search
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
      <Paper>
        {loading ? (
          <Box sx={{ height: 160, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <CircularProgress />
          </Box>
        ) : !results.length && searched ? (
          <Box sx={{ textAlign: "center", py: 6 }}>
            <Typography variant="h6" color="text.secondary">
              No results found for "{query}"
            </Typography>
          </Box>
        ) : (
          <List>
            {results.map((res, idx) => (
              <ListItem key={idx} alignItems="flex-start">
                <ListItemAvatar>
                  <Avatar
                    sx={{
                      bgcolor:
                        res.type === "file"
                          ? blue[500]
                          : res.type === "folder"
                          ? green[500]
                          : res.type === "user"
                          ? orange[500]
                          : res.type === "network"
                          ? purple[500]
                          : "#1976d2",
                    }}
                  >
                    {res.type === "file" ? (
                      <InsertDriveFileIcon />
                    ) : res.type === "folder" ? (
                      <FolderIcon />
                    ) : res.type === "user" ? (
                      <PersonIcon />
                    ) : res.type === "network" ? (
                      <WifiIcon />
                    ) : (
                      <TerminalIcon />
                    )}
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={
                    <span>
                      {res.type === "user"
                        ? (res as User).name
                        : res.type === "network"
                        ? (res as NetworkInfo).interface
                        : res.type === "terminal"
                        ? (res as any).name
                        : (res as FileEntry).name}
                      <Chip
                        label={res.type}
                        size="small"
                        color={
                          res.type === "file"
                            ? "primary"
                            : res.type === "folder"
                            ? "success"
                            : res.type === "user"
                            ? "warning"
                            : res.type === "network"
                            ? "secondary"
                            : "info"
                        }
                        sx={{ ml: 1 }}
                      />
                    </span>
                  }
                  secondary={
                    <>
                      {res.type === "user" && (
                        <span>
                          <b>Email:</b> {(res as User).email}
                          <br />
                          <b>Role:</b> {(res as User).role}
                        </span>
                      )}
                      {res.type === "file" && (
                        <span>
                          Path: {(res as FileEntry).path} <br />
                          Size: {(res as FileEntry).size
                            ? `${(res as FileEntry).size} bytes`
                            : "—"}
                        </span>
                      )}
                      {res.type === "folder" && (
                        <span>
                          Path: {(res as FileEntry).path}
                        </span>
                      )}
                      {res.type === "network" && (
                        <span>
                          IP: {(res as NetworkInfo).ip} <br />
                          Status: {(res as NetworkInfo).status}
                        </span>
                      )}
                      {res.type === "terminal" && (res as any).snippet && (
                        <pre
                          style={{
                            background: "#f9f9fa",
                            display: "inline-block",
                            padding: "2px 8px",
                            borderRadius: 4,
                            margin: 0,
                          }}
                        >
                          {(res as any).snippet}
                        </pre>
                      )}
                    </>
                  }
                />
              </ListItem>
            ))}
          </List>
        )}
      </Paper>
      <Divider sx={{ my: 3 }} />
      <Button variant="outlined" color="primary">
        Advanced Search
      </Button>
    </Box>
  );
}

export default SearchTab;
