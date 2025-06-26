import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Chip,
  Tooltip,
  CircularProgress,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Snackbar,
  Alert,
  Grid,
} from "@mui/material";
import WifiIcon from "@mui/icons-material/Wifi";
import LanIcon from "@mui/icons-material/Lan";
import LockIcon from "@mui/icons-material/Lock";
import LockOpenIcon from "@mui/icons-material/LockOpen";
import PowerSettingsNewIcon from "@mui/icons-material/PowerSettingsNew";
import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import { useNetworkInterfaces } from "../hooks/useNetwork";
import * as networkAPI from "../api/network";
import { NetworkInfo, FirewallRule } from "../types/network";

function NetworkTab() {
  const { interfaces, loading, error, refresh } = useNetworkInterfaces();
  const [openFirewall, setOpenFirewall] = useState(false);
  const [firewallRules, setFirewallRules] = useState<FirewallRule[]>([]);
  const [fwLoading, setFwLoading] = useState(false);
  const [openAddRule, setOpenAddRule] = useState(false);
  const [newRule, setNewRule] = useState<Partial<FirewallRule>>({
    name: "",
    direction: "inbound",
    protocol: "TCP",
    port: "",
    action: "allow",
  });
  const [fwError, setFwError] = useState<string | null>(null);
  const [notification, setNotification] = useState<string | null>(null);

  useEffect(() => {
    if (openFirewall) {
      setFwLoading(true);
      networkAPI
        .getFirewallRules()
        .then(setFirewallRules)
        .catch((e) => setFwError(e.message || "Failed to load firewall rules"))
        .finally(() => setFwLoading(false));
    }
  }, [openFirewall]);

  const handleConnect = async (iface: NetworkInfo) => {
    try {
      await networkAPI.connectNetwork(iface.interface);
      setNotification(`Connected to ${iface.interface}`);
      refresh();
    } catch (e: any) {
      setNotification(e.message || "Failed to connect.");
    }
  };

  const handleDisconnect = async (iface: NetworkInfo) => {
    try {
      await networkAPI.disconnectNetwork(iface.interface);
      setNotification(`Disconnected from ${iface.interface}`);
      refresh();
    } catch (e: any) {
      setNotification(e.message || "Failed to disconnect.");
    }
  };

  const handleAddRule = async () => {
    if (!newRule.name || !newRule.port) return;
    setFwLoading(true);
    try {
      await networkAPI.addFirewallRule(newRule);
      setNotification("Firewall rule added.");
      setOpenAddRule(false);
      setNewRule({
        name: "",
        direction: "inbound",
        protocol: "TCP",
        port: "",
        action: "allow",
      });
      // Refresh rules
      const rules = await networkAPI.getFirewallRules();
      setFirewallRules(rules);
    } catch (e: any) {
      setFwError(e.message || "Failed to add firewall rule.");
    }
    setFwLoading(false);
  };

  const handleDeleteRule = async (id: string) => {
    setFwLoading(true);
    try {
      await networkAPI.deleteFirewallRule(id);
      setNotification("Firewall rule deleted.");
      setFirewallRules((prev) => prev.filter((r) => r.id !== id));
    } catch (e: any) {
      setFwError(e.message || "Delete failed.");
    }
    setFwLoading(false);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Network & Security
      </Typography>
      <Paper>
        {loading ? (
          <Box sx={{ height: 160, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          <List>
            {interfaces.map((iface) => (
              <ListItem
                key={iface.interface}
                secondaryAction={
                  iface.status === "connected" ? (
                    <Tooltip title="Disconnect">
                      <IconButton
                        color="error"
                        onClick={() => handleDisconnect(iface)}
                      >
                        <PowerSettingsNewIcon />
                      </IconButton>
                    </Tooltip>
                  ) : (
                    <Tooltip title="Connect">
                      <IconButton
                        color="primary"
                        onClick={() => handleConnect(iface)}
                      >
                        <PowerSettingsNewIcon />
                      </IconButton>
                    </Tooltip>
                  )
                }
              >
                <ListItemIcon>
                  {iface.type === "wifi" ? (
                    <WifiIcon color="primary" />
                  ) : (
                    <LanIcon color="info" />
                  )}
                </ListItemIcon>
                <ListItemText
                  primary={
                    <span>
                      {iface.interface}{" "}
                      <Chip
                        size="small"
                        color={
                          iface.status === "connected"
                            ? "success"
                            : iface.status === "error"
                            ? "error"
                            : "info"
                        }
                        label={iface.status}
                        sx={{ ml: 1, textTransform: "capitalize" }}
                      />
                    </span>
                  }
                  secondary={
                    <>
                      IP: {iface.ip} • MAC: {iface.mac}
                      {iface.ssid && (
                        <>
                          <br />
                          SSID: {iface.ssid}
                        </>
                      )}
                      {iface.signalStrength !== undefined && (
                        <>
                          <br />
                          Signal: {iface.signalStrength}%
                        </>
                      )}
                      {iface.speedMbps !== undefined && (
                        <>
                          <br />
                          Speed: {iface.speedMbps} Mbps
                        </>
                      )}
                    </>
                  }
                />
              </ListItem>
            ))}
          </List>
        )}
      </Paper>
      <Box sx={{ mt: 2 }}>
        <Button
          variant="contained"
          color="secondary"
          startIcon={<LockIcon />}
          onClick={() => setOpenFirewall(true)}
        >
          Manage Firewall
        </Button>
      </Box>
      {/* Firewall Dialog */}
      <Dialog
        open={openFirewall}
        onClose={() => setOpenFirewall(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Firewall Rules
          <Tooltip title="Add Rule">
            <IconButton
              color="primary"
              sx={{ ml: 2 }}
              onClick={() => setOpenAddRule(true)}
            >
              <AddIcon />
            </IconButton>
          </Tooltip>
        </DialogTitle>
        <DialogContent>
          {fwLoading ? (
            <Box sx={{ height: 120, display: "flex", alignItems: "center", justifyContent: "center" }}>
              <CircularProgress />
            </Box>
          ) : fwError ? (
            <Alert severity="error">{fwError}</Alert>
          ) : firewallRules.length === 0 ? (
            <Typography>No firewall rules.</Typography>
          ) : (
            <List>
              {firewallRules.map((rule) => (
                <ListItem
                  key={rule.id}
                  secondaryAction={
                    <Tooltip title="Delete">
                      <IconButton
                        color="error"
                        onClick={() => handleDeleteRule(rule.id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Tooltip>
                  }
                >
                  <ListItemIcon>
                    {rule.action === "allow" ? (
                      <LockOpenIcon color="success" />
                    ) : (
                      <LockIcon color="error" />
                    )}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <span>
                        {rule.name}{" "}
                        <Chip
                          label={rule.action}
                          size="small"
                          color={rule.action === "allow" ? "success" : "error"}
                          sx={{ ml: 1, textTransform: "capitalize" }}
                        />
                        <Chip
                          label={rule.direction}
                          size="small"
                          color="info"
                          sx={{ ml: 1, textTransform: "capitalize" }}
                        />
                        <Chip
                          label={rule.protocol}
                          size="small"
                          color="primary"
                          sx={{ ml: 1, textTransform: "uppercase" }}
                        />
                        <Chip
                          label={`Port: ${rule.port}`}
                          size="small"
                          color="warning"
                          sx={{ ml: 1 }}
                        />
                      </span>
                    }
                  />
                </ListItem>
              ))}
            </List>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenFirewall(false)}>Close</Button>
        </DialogActions>
        {/* Add Rule Dialog */}
        <Dialog
          open={openAddRule}
          onClose={() => setOpenAddRule(false)}
          maxWidth="xs"
          fullWidth
        >
          <DialogTitle>Add Firewall Rule</DialogTitle>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  label="Rule Name"
                  fullWidth
                  value={newRule.name}
                  onChange={(e) =>
                    setNewRule((r) => ({ ...r, name: e.target.value }))
                  }
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Port"
                  fullWidth
                  value={newRule.port}
                  onChange={(e) =>
                    setNewRule((r) => ({ ...r, port: e.target.value }))
                  }
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  select
                  label="Direction"
                  value={newRule.direction}
                  onChange={(e) =>
                    setNewRule((r) => ({
                      ...r,
                      direction: e.target.value as "inbound" | "outbound",
                    }))
                  }
                  fullWidth
                >
                  <MenuItem value="inbound">Inbound</MenuItem>
                  <MenuItem value="outbound">Outbound</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={6}>
                <TextField
                  select
                  label="Protocol"
                  value={newRule.protocol}
                  onChange={(e) =>
                    setNewRule((r) => ({
                      ...r,
                      protocol: e.target.value as string,
                    }))
                  }
                  fullWidth
                >
                  <MenuItem value="TCP">TCP</MenuItem>
                  <MenuItem value="UDP">UDP</MenuItem>
                  <MenuItem value="ICMP">ICMP</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  select
                  label="Action"
                  value={newRule.action}
                  onChange={(e) =>
                    setNewRule((r) => ({
                      ...r,
                      action: e.target.value as "allow" | "deny",
                    }))
                  }
                  fullWidth
                >
                  <MenuItem value="allow">Allow</MenuItem>
                  <MenuItem value="deny">Deny</MenuItem>
                </TextField>
              </Grid>
            </Grid>
            {fwError && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {fwError}
              </Alert>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenAddRule(false)}>Cancel</Button>
            <Button
              onClick={handleAddRule}
              disabled={fwLoading || !newRule.name || !newRule.port}
            >
              Add
            </Button>
          </DialogActions>
        </Dialog>
      </Dialog>
      {/* Notifications */}
      <Snackbar
        open={!!notification}
        autoHideDuration={2500}
        onClose={() => setNotification(null)}
      >
        <Alert
          severity="success"
          sx={{ width: "100%" }}
        >
          {notification}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default NetworkTab;
