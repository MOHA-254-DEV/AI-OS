import { useState, useEffect } from "react";
import * as systemAPI from "../api/system";
import { SystemStats } from "../types/system";

export function useSystemStats() {
  const [stats, setStats] = useState<SystemStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await systemAPI.getSystemStats();
      setStats(data);
    } catch (e: any) {
      setError(e.message || "Failed to load system stats.");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 10000); // Refresh every 10s
    return () => clearInterval(interval);
  }, []);

  return { stats, loading, error, refresh: fetchStats };
}
