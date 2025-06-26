import React, { createContext, useState, useContext } from "react";
import { SystemStats } from "../types/system";
import { NetworkInfo } from "../types/network";

interface OSContextProps {
  systemStats: SystemStats | null;
  setSystemStats: (stats: SystemStats) => void;
  networkInfo: NetworkInfo[] | null;
  setNetworkInfo: (nets: NetworkInfo[]) => void;
  notifications: string[];
  addNotification: (message: string) => void;
}

const OSContext = createContext<OSContextProps | undefined>(undefined);

export const OSProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [systemStats, setSystemStats] = useState<SystemStats | null>(null);
  const [networkInfo, setNetworkInfo] = useState<NetworkInfo[] | null>(null);
  const [notifications, setNotifications] = useState<string[]>([]);

  const addNotification = (msg: string) => setNotifications((prev) => [...prev, msg]);

  return (
    <OSContext.Provider
      value={{
        systemStats,
        setSystemStats,
        networkInfo,
        setNetworkInfo,
        notifications,
        addNotification,
      }}
    >
      {children}
    </OSContext.Provider>
  );
};

export function useOS() {
  const ctx = useContext(OSContext);
  if (!ctx) throw new Error("useOS must be used inside OSProvider");
  return ctx;
}
