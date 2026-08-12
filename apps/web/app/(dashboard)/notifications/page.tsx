"use client";

import { useState } from "react";
import { NotificationHeader } from "@/components/notifications/NotificationHeader";
import { NotificationTable } from "@/components/notifications/NotificationTable";
import type {
  Notification,
  NotificationStatus,
  NotificationType,
} from "@/components/notifications/data/notification-data";
import { useNotificationStore } from "@/lib/store/notification-store";

export default function NotificationsPage() {
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState<
    NotificationType | "all"
  >("all");
  const [statusFilter, setStatusFilter] = useState<
    NotificationStatus | "all"
  >("all");

  const notifications = useNotificationStore(
    (state) => state.notifications,
  );
  const isLoading = useNotificationStore(
    (state) => state.isLoading,
  );
  const error = useNotificationStore((state) => state.error);
  const markAsRead = useNotificationStore(
    (state) => state.markAsRead,
  );
  const markAllAsRead = useNotificationStore(
    (state) => state.markAllAsRead,
  );
  const deleteNotification = useNotificationStore(
    (state) => state.deleteNotification,
  );
  const clearError = useNotificationStore(
    (state) => state.clearError,
  );

  const query = search.trim().toLowerCase();

  const filteredNotifications = notifications.filter(
    (notification) => {
      const matchesSearch =
        !query ||
        [
          notification.title,
          notification.message,
          notification.type,
          notification.status,
        ].some((value) => value.toLowerCase().includes(query));

      const matchesType =
        typeFilter === "all" || notification.type === typeFilter;

      const matchesStatus =
        statusFilter === "all" ||
        notification.status === statusFilter;

      return matchesSearch && matchesType && matchesStatus;
    },
  );

  const handleMarkAsRead = (notification: Notification) => {
    markAsRead(notification.id);
  };

  const handleDeleteNotification = (
    notification: Notification,
  ) => {
    deleteNotification(notification.id);
  };

  return (
    <section className="space-y-6">
      <NotificationHeader
        search={search}
        typeFilter={typeFilter}
        statusFilter={statusFilter}
        onSearchChange={setSearch}
        onTypeFilterChange={setTypeFilter}
        onStatusFilterChange={setStatusFilter}
        onMarkAllAsRead={markAllAsRead}
      />

      {error ? (
        <div role="alert">
          <p>{error}</p>
          <button type="button" onClick={clearError}>
            Dismiss
          </button>
        </div>
      ) : null}

      {isLoading ? (
        <p>Loading notifications...</p>
      ) : (
        <NotificationTable
          notifications={filteredNotifications}
          onMarkAsRead={handleMarkAsRead}
          onDeleteNotification={handleDeleteNotification}
        />
      )}
    </section>
  );
}
