import axios from "axios";
import { API_BASE } from "../utils/config";
import { NetworkInfo, FirewallRule } from "../types/network";

// Get all network interfaces
export async function getNetworkInfo(): Promise<NetworkInfo[]> {
  const token = localStorage.getItem("token");
  const res = await axios.get(`${API_BASE}/network/interfaces`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data.interfaces;
}

// Connect/disconnect network
export async function connectNetwork(interfaceName: string): Promise<void> {
  const token = localStorage.getItem("token");
  await axios.post(`${API_BASE}/network/connect`, { interface: interfaceName }, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function disconnectNetwork(interfaceName: string): Promise<void> {
  const token = localStorage.getItem("token");
  await axios.post(`${API_BASE}/network/disconnect`, { interface: interfaceName }, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

// Get firewall rules
export async function getFirewallRules(): Promise<FirewallRule[]> {
  const token = localStorage.getItem("token");
  const res = await axios.get(`${API_BASE}/network/firewall`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data.rules;
}

// Add firewall rule
export async function addFirewallRule(rule: Partial<FirewallRule>): Promise<FirewallRule> {
  const token = localStorage.getItem("token");
  const res = await axios.post(`${API_BASE}/network/firewall`, rule, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data.rule;
}

// Remove firewall rule
export async function deleteFirewallRule(id: string): Promise<void> {
  const token = localStorage.getItem("token");
  await axios.delete(`${API_BASE}/network/firewall/${id}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}
