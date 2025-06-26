import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Grid,
  Avatar,
  LinearProgress,
  Divider,
  Paper,
  List,
  ListItem,
  ListItemText,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
  Tooltip,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Snackbar,
  Alert,
} from "@mui/material";
import MemoryIcon from "@mui/icons-material/Memory";
import StorageIcon from "@mui/icons-material/Storage";
import NetworkCheckIcon from "@mui/icons-material/NetworkCheck";
import SecurityIcon from "@mui/icons-material/Security";
import UpdateIcon from "@mui/icons-material/Update";
import CloseIcon from "@mui/icons-material/Close";
import AutorenewIcon from "@mui/icons-material/Autorenew";
import { useSystemStats } from "../hooks/useSystem";
import { runSystemUpdate, getProcesses } from "../api/system";
import { formatBytes, formatDate } from "../utils/helpers";
import { SystemStats, ProcessInfo } from "../types/system";

function SystemTab() {
  const { stats, loading, error, refresh } = useSystemStats();
  const [tab, setTab] = useState(0);
  const [openUpdate, setOpenUpdate] = useState(false);
  const [note, setNote] = useState("");
  const [updateLoading, setUpdateLoading] = useState(false);
  const [updateResult, setUpdateResult] = useState<string | null>(null);
  const [processes, setProcesses] = useState<ProcessInfo[]>([]);
  const [procLoading, setProcLoading] = useState(false);

  useEffect(() => {
    if (tab === 1) {
      setProcLoading(true);
      getProcesses()
        .then(setProcesses)
        .finally(() => setProcLoading(false));
    }
  }, [tab]);

  const handleRunUpdate = async () => {
    setUpdateLoading(true);
    try {
      const result = await runSystemUpdate();
      setUpdateResult(result.result);
    } catch (e: any) {
      setUpdateResult(e.message || "Update failed.");
    }
    setUpdateLoading(false);
    setOpenUpdate(false);
  };

  if (loading) return <Typography>Loading system info...</Typography>;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!stats) return <Alert severity="warning">No system data found.</Alert>;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        System Dashboard
      </Typography>
      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 2 }}>
        <Tab label="Overview" />
        <Tab label="Processes" />
        <Tab label="Events" />
      </Tabs>
      {tab === 0 && (
        <>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={2.4}>
              <Card sx={{ minWidth: 200, bgcolor: "#f5fafd" }}>
                <CardContent>
                  <Avatar sx={{ bgcolor: "#1565c0", mb: 2 }}>
                    <MemoryIcon />
                  </Avatar>
                  <Typography variant="h6">CPU Usage</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {stats.cpuUsage}% used
                  </Typography>
                  <LinearProgress value={stats.cpuUsage} variant="determinate" sx={{ height: 10, my: 1, borderRadius: 5 }} color="primary" />
                </CardContent>
                <CardActions>
                  <Button size="small" startIcon={<AutorenewIcon />} onClick={refresh}>Refresh</Button>
                </CardActions>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={2.4}>
              <Card sx={{ minWidth: 200, bgcolor: "#f5fafd" }}>
                <CardContent>
                  <Avatar sx={{ bgcolor: "#388e3c", mb: 2 }}>
                    <MemoryIcon />
                  </Avatar>
                  <Typography variant="h6">RAM Usage</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {stats.ramUsage}% used
                  </Typography>
                  <LinearProgress value={stats.ramUsage} variant="determinate" sx={{ height: 10, my: 1, borderRadius: 5 }} color="success" />
                </CardContent>
                <CardActions>
                  <Button size="small" startIcon={<AutorenewIcon />} onClick={refresh}>Refresh</Button>
                </CardActions>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={2.4}>
              <Card sx={{ minWidth: 200, bgcolor: "#fffde7" }}>
                <CardContent>
                  <Avatar sx={{ bgcolor: "#fbc02d", mb: 2 }}>
                    <StorageIcon />
                  </Avatar>
                  <Typography variant="h6">Disk Usage</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {stats.diskUsage}% used
                  </Typography>
                  <LinearProgress value={stats.diskUsage} variant="determinate" sx={{ height: 10, my: 1, borderRadius: 5 }} color="warning" />
                </CardContent>
                <CardActions>
                  <Button size="small" startIcon={<AutorenewIcon />} onClick={refresh}>Refresh</Button>
                </CardActions>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={2.4}>
              <Card sx={{ minWidth: 200, bgcolor: "#e0f7fa" }}>
                <CardContent>
                  <Avatar sx={{ bgcolor: "#00838f", mb: 2 }}>
                    <NetworkCheckIcon />
                  </Avatar>
                  <Typography variant="h6">Network</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {stats.netUsage}% usage
                  </Typography>
                  <LinearProgress value={stats.netUsage} variant="determinate" sx={{ height: 10, my: 1, borderRadius: 5 }} color="info" />
                </CardContent>
                <CardActions>
                  <Button size="small" startIcon={<AutorenewIcon />} onClick={refresh}>Refresh</Button>
                </CardActions>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={2.4}>
              <Card sx={{ minWidth: 200, bgcolor: "#ffebee" }}>
                <CardContent>
                  <Avatar sx={{ bgcolor: "#d32f2f", mb: 2 }}>
                    <SecurityIcon />
                  </Avatar>
                  <Typography variant="h6">Security</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Secure
                  </Typography>
                  <Chip label="Firewall Active" color="success" />
                </CardContent>
                <CardActions>
                  <Button size="small" startIcon={<UpdateIcon />} onClick={() => setOpenUpdate(true)}>
                    Update
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          </Grid>
          <Divider sx={{ my: 3 }} />
          <Typography variant="h6" gutterBottom>
            Uptime
          </Typography>
          <Chip label={`${Math.floor(stats.uptime / 3600)}h ${Math.floor((stats.uptime % 3600) / 60)}m`} color="primary" sx={{ fontSize: 18, mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            Load Average
          </Typography>
          <Paper sx={{ maxWidth: 400, mb: 3, p: 2 }}>
            {stats.loadAvg.map((l, i) => (
              <Chip key={i} label={l.toFixed(2)} sx={{ mr: 1 }} />
            ))}
          </Paper>
        </>
      )}
      {tab === 1 && (
        <>
          <Typography variant="h6" gutterBottom>
            Running Processes
          </Typography>
          {procLoading ? (
            <Typography>Loading processes...</Typography>
          ) : (
            <TableContainer component={Paper}>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>PID</TableCell>
                    <TableCell>Name</TableCell>
                    <TableCell>User</TableCell>
                    <TableCell>CPU %</TableCell>
                    <TableCell>RAM %</TableCell>
                    <TableCell>Started</TableCell>
                    <TableCell>Command</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {processes.map((proc) => (
                    <TableRow key={proc.pid}>
                      <TableCell>{proc.pid}</TableCell>
                      <TableCell>{proc.name}</TableCell>
                      <TableCell>{proc.user}</TableCell>
                      <TableCell>{proc.cpu.toFixed(1)}</TableCell>
                      <TableCell>{proc.mem.toFixed(1)}</TableCell>
                      <TableCell>{formatDate(proc.started)}</TableCell>
                      <TableCell>
                        <Tooltip title={proc.command}>
                          <span style={{ maxWidth: 120, display: "inline-block", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                            {proc.command}
                          </span>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </>
      )}
      {tab === 2 && (
        <>
          <Typography variant="h6" gutterBottom>
            Recent Events
          </Typography>
          <Paper sx={{ maxWidth: 500, mb: 3 }}>
            <List>
              <ListItem>
                <ListItemText primary="System started" secondary={formatDate(new Date(Date.now() - stats.uptime * 1000))} />
              </ListItem>
              <ListItem>
                <ListItemText primary="AI Agent connected" secondary={formatDate(new Date())} />
              </ListItem>
              <ListItem>
                <ListItemText primary="Security scan passed" secondary={formatDate(new Date())} />
              </ListItem>
              <ListItem>
                <ListItemText primary="Update check complete" secondary={formatDate(new Date())} />
              </ListItem>
            </List>
          </Paper>
        </>
      )}
      <Box mb={4}>
        <img
          src="/images/desktop_preview.png"
          alt="Desktop Preview"
          width="100%"
          style={{ borderRadius: 12, maxHeight: 320, objectFit: "cover" }}
        />
      </Box>
      <Dialog open={openUpdate} onClose={() => setOpenUpdate(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          System Update
          <IconButton
            aria-label="close"
            onClick={() => setOpenUpdate(false)}
            sx={{ position: "absolute", right: 8, top: 8, color: "#aaa" }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          <Typography gutterBottom>
            A new system update is available. Would you like to install now?
          </Typography>
          <TextField
            label="Admin Note"
            fullWidth
            value={note}
            onChange={(e) => setNote(e.target.value)}
            margin="normal"
            multiline
            minRows={3}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenUpdate(false)} color="primary">
            Cancel
          </Button>
          <Button onClick={handleRunUpdate} color="secondary" disabled={updateLoading}>
            {updateLoading ? <AutorenewIcon className="spin" /> : "Install"}
          </Button>
        </DialogActions>
      </Dialog>
      <Snackbar
        open={!!updateResult}
        autoHideDuration={4000}
        onClose={() => setUpdateResult(null)}
      >
        <Alert severity={updateResult?.toLowerCase().includes("fail") ? "error" : "success"} sx={{ width: "100%" }}>
          {updateResult}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default SystemTab;
