import axios from "axios";
import { API_BASE } from "../utils/config";
import { FileEntry } from "../types/files";

// List files in a directory
export async function listFiles(path: string): Promise<FileEntry[]> {
  const token = localStorage.getItem("token");
  const res = await axios.get(`${API_BASE}/files`, {
    headers: { Authorization: `Bearer ${token}` },
    params: { path },
  });
  return res.data.files;
}

// Upload file to a directory
export async function uploadFile(path: string, file: File): Promise<FileEntry> {
  const token = localStorage.getItem("token");
  const formData = new FormData();
  formData.append("file", file);
  formData.append("path", path);
  const res = await axios.post(`${API_BASE}/files/upload`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`,
    },
  });
  return res.data.file;
}

// Download file as blob
export async function downloadFile(path: string): Promise<Blob> {
  const token = localStorage.getItem("token");
  const res = await axios.get(`${API_BASE}/files/download`, {
    headers: { Authorization: `Bearer ${token}` },
    params: { path },
    responseType: "blob",
  });
  return res.data;
}

// Delete file or folder
export async function deleteFile(path: string): Promise<void> {
  const token = localStorage.getItem("token");
  await axios.delete(`${API_BASE}/files`, {
    headers: { Authorization: `Bearer ${token}` },
    data: { path },
  });
}
