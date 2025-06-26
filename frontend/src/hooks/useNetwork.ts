import { useState, useEffect } from "react";
import * as networkAPI from "../api/network";
import { NetworkInfo } from "../types/network";

export function useNetworkInterfaces() {
  const [interfaces, setInterfaces] = useState<NetworkInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = async () => {
    setLoading(true);
    setError(null);
    try {
      const nets = await networkAPI.getNetworkInfo();
      setInterfaces(nets);
    } catch (e: any) {
      setError(e.message || "Failed to load network info.");
    }
    setLoading(false);
  };

  useEffect(() => {
    refresh();
  }, []);

  return { interfaces, loading, error, refresh };
}
