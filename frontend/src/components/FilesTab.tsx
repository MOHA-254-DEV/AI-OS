import React, { useState, useEffect, useCallback } from "react";
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Divider,
  Breadcrumbs,
  Link,
  Paper,
  Avatar,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Menu,
  MenuItem,
  Tooltip,
  Grid,
  Snackbar,
  Alert,
  CircularProgress,
  Backdrop,
} from "@mui/material";
import FolderIcon from "@mui/icons-material/Folder";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";
import CreateNewFolderIcon from "@mui/icons-material/CreateNewFolder";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import DeleteIcon from "@mui/icons-material/Delete";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import DownloadIcon from "@mui/icons-material/Download";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import PreviewIcon from "@mui/icons-material/Preview";
import { useFiles } from "../hooks/useFiles";
import * as filesAPI from "../api/files";
import { FileEntry } from "../types/files";
import { formatBytes, formatDate } from "../utils/helpers";

const initialPath = ["Home"];

function FilesTab() {
  const [currentPath, setCurrentPath] = useState(initialPath);
  const [openNewFolder, setOpenNewFolder] = useState(false);
  const [newFolderName, setNewFolderName] = useState("");
  const [fileMenuAnchor, setFileMenuAnchor] = useState<null | HTMLElement>(null);
  const [selectedFile, setSelectedFile] = useState<FileEntry | null>(null);
  const [openDelete, setOpenDelete] = useState(false);
  const [openPreview, setOpenPreview] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [fileToUpload, setFileToUpload] = useState<File | null>(null);
  const [notification, setNotification] = useState<string | null>(null);

  const pathStr = currentPath.join("/");
  const { files, loading, error, refresh } = useFiles(pathStr);

  // Handle folder navigation
  const handleEnterFolder = (folder: string) => {
    setCurrentPath([...currentPath, folder]);
  };

  const handleBreadcrumbClick = (idx: number) => {
    setCurrentPath(currentPath.slice(0, idx + 1));
  };

  // New folder creation
  const handleNewFolder = async () => {
    if (!newFolderName.trim()) return;
    setUploading(true);
    try {
      await filesAPI.uploadFile(pathStr, new File([], newFolderName)); // Backend should treat this as folder if file empty and type folder
      setNotification(`Folder "${newFolderName}" created.`);
      refresh(pathStr);
    } catch (e: any) {
      setNotification(e.message || "Failed to create folder.");
    }
    setOpenNewFolder(false);
    setNewFolderName("");
    setUploading(false);
  };

  // File upload
  const handleUpload = async () => {
    if (!fileToUpload) return;
    setUploading(true);
    try {
      await filesAPI.uploadFile(pathStr, fileToUpload);
      setNotification(`File "${fileToUpload.name}" uploaded.`);
      refresh(pathStr);
    } catch (e: any) {
      setNotification(e.message || "Upload failed.");
    }
    setFileToUpload(null);
    setUploading(false);
  };

  // File menu (open, delete, download, preview)
  const handleFileMenu = (e: React.MouseEvent, file: FileEntry) => {
    setFileMenuAnchor(e.currentTarget);
    setSelectedFile(file);
  };
  const handleFileMenuClose = () => {
    setFileMenuAnchor(null);
    setSelectedFile(null);
  };

  // Delete file/folder
  const handleDelete = async () => {
    if (!selectedFile) return;
    setUploading(true);
    try {
      await filesAPI.deleteFile(selectedFile.path);
      setNotification(`${selectedFile.type === "folder" ? "Folder" : "File"} "${selectedFile.name}" deleted.`);
      refresh(pathStr);
    } catch (e: any) {
      setNotification(e.message || "Delete failed.");
    }
    setOpenDelete(false);
    setUploading(false);
    setFileMenuAnchor(null);
    setSelectedFile(null);
  };

  // Download file
  const handleDownload = async () => {
    if (!selectedFile) return;
    setUploading(true);
    try {
      const blob = await filesAPI.downloadFile(selectedFile.path);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = selectedFile.name;
      a.click();
      setNotification(`Downloading "${selectedFile.name}"`);
    } catch (e: any) {
      setNotification(e.message || "Download failed.");
    }
    setUploading(false);
    setFileMenuAnchor(null);
    setSelectedFile(null);
  };

  // Preview file
  const handlePreview = () => {
    setOpenPreview(true);
    setFileMenuAnchor(null);
  };

  // Effect: refresh files when path changes
  useEffect(() => {
    refresh(currentPath.join("/"));
  }, [currentPath, refresh]);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        File Explorer
      </Typography>
      <Breadcrumbs sx={{ mb: 2 }}>
        {currentPath.map((dir, idx) => (
          <Link
            key={dir}
            underline="hover"
            color="inherit"
            onClick={() => handleBreadcrumbClick(idx)}
            sx={{ cursor: "pointer" }}
          >
            {dir}
          </Link>
        ))}
      </Breadcrumbs>
      <Paper sx={{ mb: 3, p: 2 }}>
        <Grid container spacing={2}>
          <Grid item>
            <Button
              variant="contained"
              startIcon={<CreateNewFolderIcon />}
              onClick={() => setOpenNewFolder(true)}
              disabled={uploading}
            >
              New Folder
            </Button>
          </Grid>
          <Grid item>
            <Button
              variant="outlined"
              startIcon={<UploadFileIcon />}
              component="label"
              disabled={uploading}
            >
              Upload
              <input
                type="file"
                hidden
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    setFileToUpload(e.target.files[0]);
                  }
                }}
              />
            </Button>
            {fileToUpload && (
              <Button
                variant="outlined"
                color="success"
                sx={{ ml: 1 }}
                onClick={handleUpload}
                disabled={uploading}
              >
                Confirm Upload: {fileToUpload.name}
              </Button>
            )}
          </Grid>
        </Grid>
      </Paper>
      <Paper>
        {loading ? (
          <Box sx={{ height: 200, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          <List>
            {files.map((file) => (
              <ListItem
                key={file.name}
                secondaryAction={
                  <>
                    <Tooltip title="More">
                      <IconButton
                        edge="end"
                        onClick={(e) => handleFileMenu(e, file)}
                      >
                        <MoreVertIcon />
                      </IconButton>
                    </Tooltip>
                    <Menu
                      anchorEl={fileMenuAnchor}
                      open={Boolean(fileMenuAnchor && selectedFile === file)}
                      onClose={handleFileMenuClose}
                    >
                      {file.type === "file" && (
                        <MenuItem onClick={handlePreview}>
                          <PreviewIcon sx={{ mr: 1 }} fontSize="small" /> Preview
                        </MenuItem>
                      )}
                      <MenuItem
                        onClick={() => {
                          setOpenDelete(true);
                          handleFileMenuClose();
                        }}
                      >
                        <DeleteIcon sx={{ mr: 1 }} fontSize="small" /> Delete
                      </MenuItem>
                      {file.type === "file" && (
                        <MenuItem onClick={handleDownload}>
                          <DownloadIcon sx={{ mr: 1 }} fontSize="small" /> Download
                        </MenuItem>
                      )}
                    </Menu>
                  </>
                }
                sx={{
                  "&:hover": { background: "#e3f2fd" },
                  cursor: file.type === "folder" ? "pointer" : "default",
                }}
                onClick={() =>
                  file.type === "folder" ? handleEnterFolder(file.name) : undefined
                }
              >
                <ListItemIcon>
                  {file.type === "folder" ? (
                    <FolderIcon color="primary" />
                  ) : (
                    <InsertDriveFileIcon color="action" />
                  )}
                </ListItemIcon>
                <ListItemText
                  primary={file.name}
                  secondary={`${formatDate(file.modified)}${file.size ? ` • ${formatBytes(file.size)}` : ""}`}
                />
              </ListItem>
            ))}
          </List>
        )}
      </Paper>
      {/* New Folder Dialog */}
      <Dialog
        open={openNewFolder}
        onClose={() => setOpenNewFolder(false)}
        maxWidth="xs"
        fullWidth
      >
        <DialogTitle>New Folder</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Folder Name"
            fullWidth
            value={newFolderName}
            onChange={(e) => setNewFolderName(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenNewFolder(false)}>Cancel</Button>
          <Button onClick={handleNewFolder} disabled={uploading || !newFolderName.trim()}>
            Create
          </Button>
        </DialogActions>
      </Dialog>
      {/* Delete Modal */}
      <Dialog
        open={openDelete}
        onClose={() => setOpenDelete(false)}
        maxWidth="xs"
        fullWidth
      >
        <DialogTitle>Delete {selectedFile?.name}?</DialogTitle>
        <DialogContent>
          <Typography>
            This action cannot be undone. Are you sure you want to delete{" "}
            <b>{selectedFile?.name}</b>?
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDelete(false)}>Cancel</Button>
          <Button color="error" onClick={handleDelete} disabled={uploading}>
            Delete
          </Button>
        </DialogActions>
      </Dialog>
      {/* Preview Modal */}
      <Dialog open={openPreview} onClose={() => setOpenPreview(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Preview: {selectedFile?.name}
          <IconButton
            aria-label="close"
            onClick={() => setOpenPreview(false)}
            sx={{ position: "absolute", right: 8, top: 8, color: "#aaa" }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          {/* For demo, just show name/type. Expand with file viewer based on mimeType */}
          {selectedFile?.previewUrl ? (
            <img src={selectedFile.previewUrl} alt={selectedFile.name} style={{ width: "100%", maxHeight: 400, objectFit: "contain" }} />
          ) : (
            <Typography variant="body2">Cannot preview this file type.</Typography>
          )}
        </DialogContent>
      </Dialog>
      {/* Uploading Backdrop */}
      <Backdrop open={uploading} sx={{ zIndex: 2000, color: "#fff" }}>
        <CircularProgress color="inherit" />
      </Backdrop>
      {/* Notifications */}
      <Snackbar
        open={!!notification}
        autoHideDuration={3000}
        onClose={() => setNotification(null)}
      >
        <Alert severity="success" sx={{ width: "100%" }}>
          {notification}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default FilesTab;
