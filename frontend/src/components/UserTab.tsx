import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Avatar,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Tooltip,
  Chip,
  MenuItem,
  Snackbar,
  Alert,
  CircularProgress,
  Select,
  InputLabel,
  FormControl,
  Divider,
} from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import AddIcon from "@mui/icons-material/Add";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { blue, green, orange, red } from "@mui/material/colors";
import { listUsers, addUser, editUser, deleteUser } from "../api/users";
import { User, UserRole } from "../types/user";
import { isValidEmail } from "../utils/validators";

const roleColors: Record<UserRole, string> = {
  admin: red[400],
  agent: green[400],
  user: blue[400],
};

const roleLabels: Record<UserRole, string> = {
  admin: "Admin",
  agent: "AI Agent",
  user: "User",
};

const emptyUser: User = {
  id: "",
  name: "",
  email: "",
  role: "user",
  avatarUrl: "",
  registered: "",
  lastLogin: "",
  status: "active",
};

const roles: UserRole[] = ["admin", "agent", "user"];

function UserTab() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [openAdd, setOpenAdd] = useState(false);
  const [openEdit, setOpenEdit] = useState(false);
  const [currentUser, setCurrentUser] = useState<User>(emptyUser);
  const [form, setForm] = useState<User>({ ...emptyUser });
  const [formError, setFormError] = useState<string>("");
  const [openDelete, setOpenDelete] = useState(false);
  const [notification, setNotification] = useState<string | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<User | null>(null);

  // Fetch users on mount
  useEffect(() => {
    setLoading(true);
    listUsers()
      .then(setUsers)
      .finally(() => setLoading(false));
  }, []);

  // Add user
  const handleAdd = async () => {
    setFormError("");
    if (!form.name || !form.email || !form.role) {
      setFormError("All fields required.");
      return;
    }
    if (!isValidEmail(form.email)) {
      setFormError("Invalid email format.");
      return;
    }
    try {
      const newUser = await addUser(form);
      setUsers((prev) => [...prev, newUser]);
      setOpenAdd(false);
      setForm({ ...emptyUser });
      setNotification("User added.");
    } catch (e: any) {
      setFormError(e.message || "Failed to add user.");
    }
  };

  // Edit user
  const handleEdit = async () => {
    setFormError("");
    if (!form.name || !form.email || !form.role) {
      setFormError("All fields required.");
      return;
    }
    if (!isValidEmail(form.email)) {
      setFormError("Invalid email format.");
      return;
    }
    try {
      const updated = await editUser(form.id, form);
      setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)));
      setOpenEdit(false);
      setCurrentUser(emptyUser);
      setForm({ ...emptyUser });
      setNotification("User updated.");
    } catch (e: any) {
      setFormError(e.message || "Failed to update user.");
    }
  };

  // Delete user
  const handleDelete = async () => {
    if (!deleteTarget) return;
    try {
      await deleteUser(deleteTarget.id);
      setUsers((prev) => prev.filter((u) => u.id !== deleteTarget.id));
      setOpenDelete(false);
      setNotification("User deleted.");
    } catch (e: any) {
      setNotification(e.message || "Failed to delete user.");
    }
  };

  // Prepare edit
  const handleEditOpen = (user: User) => {
    setCurrentUser(user);
    setForm(user);
    setOpenEdit(true);
    setFormError("");
  };

  // Prepare delete
  const handleDeleteOpen = (user: User) => {
    setDeleteTarget(user);
    setOpenDelete(true);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        User Management
      </Typography>
      <Paper>
        {loading ? (
          <Box sx={{ height: 160, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <CircularProgress />
          </Box>
        ) : (
          <List>
            {users.map((user) => (
              <ListItem
                key={user.id}
                secondaryAction={
                  <>
                    <Tooltip title="Edit">
                      <IconButton
                        edge="end"
                        onClick={() => handleEditOpen(user)}
                      >
                        <EditIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Delete">
                      <IconButton
                        edge="end"
                        color="error"
                        onClick={() => handleDeleteOpen(user)}
                        disabled={user.role === "admin"}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Tooltip>
                  </>
                }
              >
                <ListItemAvatar>
                  <Avatar sx={{ bgcolor: roleColors[user.role] }}>
                    <PersonIcon />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={
                    <>
                      {user.name}{" "}
                      <Chip
                        size="small"
                        sx={{ bgcolor: roleColors[user.role], color: "#fff", ml: 1 }}
                        label={roleLabels[user.role]}
                      />
                      {user.status === "disabled" && (
                        <Chip
                          size="small"
                          color="warning"
                          label="Disabled"
                          sx={{ ml: 1 }}
                        />
                      )}
                    </>
                  }
                  secondary={
                    <>
                      <span>{user.email}</span> • Registered: {user.registered || "-"}
                      <br />
                      Last login: {user.lastLogin || "-"}
                    </>
                  }
                />
              </ListItem>
            ))}
          </List>
        )}
      </Paper>
      <Button
        variant="contained"
        startIcon={<AddIcon />}
        sx={{ mt: 2 }}
        onClick={() => {
          setForm({ ...emptyUser });
          setOpenAdd(true);
          setFormError("");
        }}
      >
        Add User
      </Button>
      {/* Add User Dialog */}
      <Dialog open={openAdd} onClose={() => setOpenAdd(false)}>
        <DialogTitle>Add User</DialogTitle>
        <DialogContent>
          <TextField
            label="Name"
            fullWidth
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            sx={{ my: 1 }}
          />
          <TextField
            label="Email"
            fullWidth
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            sx={{ my: 1 }}
          />
          <FormControl fullWidth sx={{ my: 1 }}>
            <InputLabel id="role-label">Role</InputLabel>
            <Select
              labelId="role-label"
              value={form.role}
              label="Role"
              onChange={(e) =>
                setForm({ ...form, role: e.target.value as UserRole })
              }
            >
              {roles.map((r) => (
                <MenuItem value={r} key={r}>
                  {roleLabels[r]}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          {formError && (
            <Alert severity="error" sx={{ my: 1 }}>
              {formError}
            </Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAdd(false)}>Cancel</Button>
          <Button onClick={handleAdd}>Add</Button>
        </DialogActions>
      </Dialog>
      {/* Edit User Dialog */}
      <Dialog open={openEdit} onClose={() => setOpenEdit(false)}>
        <DialogTitle>Edit User</DialogTitle>
        <DialogContent>
          <TextField
            label="Name"
            fullWidth
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            sx={{ my: 1 }}
          />
          <TextField
            label="Email"
            fullWidth
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            sx={{ my: 1 }}
          />
          <FormControl fullWidth sx={{ my: 1 }}>
            <InputLabel id="role-label-edit">Role</InputLabel>
            <Select
              labelId="role-label-edit"
              value={form.role}
              label="Role"
              onChange={(e) =>
                setForm({ ...form, role: e.target.value as UserRole })
              }
            >
              {roles.map((r) => (
                <MenuItem value={r} key={r}>
                  {roleLabels[r]}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          {formError && (
            <Alert severity="error" sx={{ my: 1 }}>
              {formError}
            </Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEdit(false)}>Cancel</Button>
          <Button onClick={handleEdit}>Save</Button>
        </DialogActions>
      </Dialog>
      {/* Delete User Dialog */}
      <Dialog open={openDelete} onClose={() => setOpenDelete(false)}>
        <DialogTitle>Delete User</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete user <b>{deleteTarget?.name}</b>? This cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDelete(false)}>Cancel</Button>
          <Button color="error" onClick={handleDelete}>
            Delete
          </Button>
        </DialogActions>
      </Dialog>
      {/* Notification */}
      <Snackbar
        open={!!notification}
        autoHideDuration={2000}
        onClose={() => setNotification(null)}
      >
        <Alert severity="success" sx={{ width: "100%" }}>
          {notification}
        </Alert>
      </Snackbar>
      <Divider sx={{ my: 3 }} />
      <Box sx={{ mt: 2 }}>
        <Typography variant="body1" color="text.secondary">
          <b>Tip:</b> AI agents can be assigned the <Chip label="AI Agent" color="success" size="small" /> role for specialized automation tasks.
        </Typography>
      </Box>
    </Box>
  );
}

export default UserTab;
