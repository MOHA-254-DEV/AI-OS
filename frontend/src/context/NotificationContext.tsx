import React, { createContext, useState, useEffect, useContext, ReactNode } from "react";
import { Notification } from "../types/notification";
import * as notificationApi from "../api/notification";

interface NotificationContextType {
  notifications: Notification[];
  refresh: () => Promise<void>;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export const NotificationProvider = ({ children }: { children: ReactNode }) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const refresh = async () => {
    const data = await notificationApi.getMyNotifications();
    setNotifications(data);
  };

  useEffect(() => {
    refresh();
  }, []);

  return (
    <NotificationContext.Provider value={{ notifications, refresh }}>
      {children}
    </NotificationContext.Provider>
  );
};

export const useNotifications = () => {
  const ctx = useContext(NotificationContext);
  if (!ctx) throw new Error("useNotifications must be used within NotificationProvider");
  return ctx;
};
