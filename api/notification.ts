import api from "../utils/apiClient";
import { Notification } from "../types/notification";

export async function getMyNotifications(): Promise<Notification[]> {
  const res = await api.get("/notifications/");
  return res.data;
}
