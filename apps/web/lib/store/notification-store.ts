import { create } from "zustand";
import {
  notificationData,
  type Notification,
} from "@/components/notifications/data/notification-data";

export interface NotificationInput {
  title: string;
  message: string;
  type: Notification["type"];
  status: Notification["status"];
  createdAt: string;
  actionUrl?: string;
}

export interface NotificationState {
  notifications: Notification[];
  isLoading: boolean;
  error: string | null;

  setNotifications: (notifications: Notification[]) => void;
  addNotification: (notification: NotificationInput) => void;
  updateNotification: (
    id: string,
    updates: Partial<NotificationInput>,
  ) => void;
  deleteNotification: (id: string) => void;
  markAsRead: (id: string) => void;
  markAllAsRead: () => void;
  clearError: () => void;
}

function getNextNotificationId(notifications: Notification[]) {
  const ids = notifications
    .map((notification) =>
      Number(notification.id.replace("NOT-", "")),
    )
    .filter(Number.isFinite);

  const nextId = Math.max(0, ...ids) + 1;

  return `NOT-${String(nextId).padStart(3, "0")}`;
}

export const useNotificationStore = create<NotificationState>(
  (set) => ({
    notifications: notificationData,
    isLoading: false,
    error: null,

    setNotifications: (notifications) => {
      set({
        notifications,
        error: null,
      });
    },

    addNotification: (notification) => {
      set((state) => ({
        notifications: [
          ...state.notifications,
          {
            ...notification,
            id: getNextNotificationId(state.notifications),
          },
        ],
        error: null,
      }));
    },

    updateNotification: (id, updates) => {
      set((state) => {
        const notificationExists = state.notifications.some(
          (notification) => notification.id === id,
        );

        if (!notificationExists) {
          return {
            error: `Notification ${id} was not found.`,
          };
        }

        return {
          notifications: state.notifications.map((notification) =>
            notification.id === id
              ? { ...notification, ...updates }
              : notification,
          ),
          error: null,
        };
      });
    },

    deleteNotification: (id) => {
      set((state) => {
        const notificationExists = state.notifications.some(
          (notification) => notification.id === id,
        );

        if (!notificationExists) {
          return {
            error: `Notification ${id} was not found.`,
          };
        }

        return {
          notifications: state.notifications.filter(
            (notification) => notification.id !== id,
          ),
          error: null,
        };
      });
    },

    markAsRead: (id) => {
      set((state) => {
        const notificationExists = state.notifications.some(
          (notification) => notification.id === id,
        );

        if (!notificationExists) {
          return {
            error: `Notification ${id} was not found.`,
          };
        }

        return {
          notifications: state.notifications.map((notification) =>
            notification.id === id
              ? { ...notification, status: "read" }
              : notification,
          ),
          error: null,
        };
      });
    },

    markAllAsRead: () => {
      set((state) => ({
        notifications: state.notifications.map((notification) => ({
          ...notification,
          status: "read",
        })),
        error: null,
      }));
    },

    clearError: () => {
      set({
        error: null,
      });
    },
  }),
);
