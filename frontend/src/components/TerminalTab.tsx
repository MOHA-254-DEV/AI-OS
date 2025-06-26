import React, { useState, useRef, useEffect } from "react";
import {
  Box,
  Typography,
  Paper,
  TextField,
  IconButton,
  Button,
  Tooltip,
  Chip,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import TerminalIcon from "@mui/icons-material/Terminal";
import ReplayIcon from "@mui/icons-material/Replay";
import ClearAllIcon from "@mui/icons-material/ClearAll";
import { blue, grey, yellow, red } from "@mui/material/colors";

// Mocked backend API call for terminal execution (replace with real API!)
async function runTerminalCommand(command: string): Promise<{ output: string; code: number }> {
  await new Promise((r) => setTimeout(r, 600));
  // Simulate responses
  if (command.trim() === "whoami") return { output: "ai-agent", code: 0 };
  if (command.trim() === "time") return { output: new Date().toLocaleString(), code: 0 };
  if (command.trim() === "clear") return { output: "", code: 0 };
  if (command.trim().startsWith("echo ")) return { output: command.trim().slice(5), code: 0 };
  if (command.trim() === "help") {
    return {
      output:
        "Available commands:\nwhoami\ntime\necho <msg>\nclear\nhelp",
      code: 0,
    };
  }
  return {
    output: `Command not found: ${command}\nType 'help' for available commands.`,
    code: 127,
  };
}

interface TerminalHistoryEntry {
  command: string;
  output: string;
  code: number;
}

const terminalTheme = {
  background: "#181a20",
  color: "#e3f2fd",
  prompt: "#00e676",
  error: yellow[700],
  user: blue[400],
};

function TerminalTab() {
  const [command, setCommand] = useState("");
  const [history, setHistory] = useState<TerminalHistoryEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [historyIdx, setHistoryIdx] = useState<number | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Keyboard UP/DOWN for cmd history
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (!["ArrowUp", "ArrowDown"].includes(e.key) || !history.length) return;
      e.preventDefault();
      if (e.key === "ArrowUp") {
        setHistoryIdx((idx) =>
          idx === null ? history.length - 1 : Math.max(0, idx - 1)
        );
      } else if (e.key === "ArrowDown") {
        setHistoryIdx((idx) =>
          idx === null
            ? null
            : idx + 1 >= history.length
            ? null
            : idx + 1
        );
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [history.length]);

  useEffect(() => {
    if (historyIdx !== null && history[historyIdx]) {
      setCommand(history[historyIdx].command);
    } else if (historyIdx === null) {
      setCommand("");
    }
    // eslint-disable-next-line
  }, [historyIdx]);

  const handleRun = async () => {
    if (!command.trim()) return;
    setLoading(true);
    const result = await runTerminalCommand(command);
    if (command.trim() === "clear") {
      setHistory([]);
      setCommand("");
      setLoading(false);
      return;
    }
    setHistory((prev) => [...prev, { command, ...result }]);
    setCommand("");
    setHistoryIdx(null);
    setLoading(false);
    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  };

  const handleClear = () => {
    setHistory([]);
    setCommand("");
    setHistoryIdx(null);
    inputRef.current?.focus();
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Terminal
      </Typography>
      <Paper
        sx={{
          background: terminalTheme.background,
          color: terminalTheme.color,
          p: 0,
          height: 400,
          overflow: "auto",
          mb: 2,
          borderRadius: 2,
        }}
      >
        <List dense sx={{ p: 1 }}>
          {history.length === 0 ? (
            <ListItem>
              <ListItemText
                primary={
                  <span style={{ color: grey[400] }}>
                    Type <code>help</code> to list available commands.
                  </span>
                }
              />
            </ListItem>
          ) : (
            history.map((h, i) => (
              <React.Fragment key={i}>
                <ListItem disablePadding>
                  <ListItemText
                    primary={
                      <span>
                        <span style={{ color: terminalTheme.prompt }}>$</span>{" "}
                        <span style={{ color: terminalTheme.user }}>
                          ai-agent
                        </span>
                        <span style={{ color: "#fff" }}>:</span>{" "}
                        <span style={{ fontWeight: 500 }}>{h.command}</span>
                      </span>
                    }
                  />
                </ListItem>
                {h.output && (
                  <ListItem
                    sx={{
                      pt: 0,
                      pb: 1,
                      whiteSpace: "pre-wrap",
                      color: h.code === 0 ? terminalTheme.color : terminalTheme.error,
                    }}
                  >
                    <ListItemText primary={h.output} />
                  </ListItem>
                )}
                <Divider sx={{ borderColor: "#23242a" }} />
              </React.Fragment>
            ))
          )}
        </List>
      </Paper>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          background: "#16171c",
          p: 1,
          borderRadius: 2,
        }}
      >
        <TerminalIcon sx={{ color: blue[400], mr: 1 }} />
        <TextField
          inputRef={inputRef}
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleRun();
          }}
          placeholder="Type command and press Enter"
          variant="standard"
          InputProps={{
            disableUnderline: true,
            sx: { color: terminalTheme.color, fontFamily: "monospace", width: "100%", pr: 2 },
          }}
          sx={{ flex: 1, mr: 2 }}
          autoFocus
        />
        <Tooltip title="Run">
          <span>
            <IconButton
              color="primary"
              onClick={handleRun}
              disabled={loading || !command.trim()}
            >
              {loading ? <CircularProgress size={22} /> : <SendIcon />}
            </IconButton>
          </span>
        </Tooltip>
        <Tooltip title="Clear">
          <span>
            <IconButton onClick={handleClear} color="warning" disabled={loading}>
              <ClearAllIcon />
            </IconButton>
          </span>
        </Tooltip>
        <Tooltip title="Replay last command">
          <span>
            <IconButton
              onClick={() => {
                if (history.length) {
                  setCommand(history[history.length - 1].command);
                  inputRef.current?.focus();
                }
              }}
              color="info"
              disabled={loading || !history.length}
            >
              <ReplayIcon />
            </IconButton>
          </span>
        </Tooltip>
      </Box>
      <Box sx={{ mt: 2 }}>
        <Chip
          label="For real shell integration, connect to your backend API."
          color="info"
          sx={{ fontSize: 14, background: "#112233", color: "#fff" }}
        />
      </Box>
    </Box>
  );
}

export default TerminalTab;
