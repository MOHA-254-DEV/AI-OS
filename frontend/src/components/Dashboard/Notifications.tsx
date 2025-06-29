import React from "react";
import { useNotifications } from "../../context/NotificationContext";
import { formatDateTime } from "../../utils/helpers";

const Notifications: React.FC = () => {
  const { notifications } = useNotifications();
  return (
    <div>
      <h2>Notifications</h2>
      <ul>
        {notifications.map((n) => (
          <li key={n.id}>
            <b>{formatDateTime(n.createdAt)}</b>: {n.message} {n.read ? "" : <span style={{ color: "red" }}>(Unread)</span>}
          </li>
        ))}
      </ul>
    </div>
  );
};
export default Notifications;
