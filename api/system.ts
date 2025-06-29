
import axios from "axios";
import { API_BASE } from "../utils/config";
import { SystemStats } from "../types/system";

// Get system stats dashboard data
export async function getSystemStats(): Promise<SystemStats> {
  const token = localStorage.getItem("token");
  const res = await axios.get(`${API_BASE}/system/stats`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}

// Run a system update
export async function runSystemUpdate(): Promise<{ result: string }> {
  const token = localStorage.getItem("token");
  const res = await axios.post(`${API_BASE}/system/update`, {}, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}

// List running system processes
export async function getProcesses(): Promise<SystemStats["processes"]> {
  const token = localStorage.getItem("token");
  const res = await axios.get(`${API_BASE}/system/processes`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data.processes;
}

