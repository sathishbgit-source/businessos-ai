"use client";

import Link from "next/link";
import { Button, StatusBadge, Table } from "@/components/ui";
import type { Notification } from "@/components/notifications/data/notification-data";

interface NotificationTableProps {
  notifications: Notification[];
  onMarkAsRead: (notification: Notification) => void;
  onDeleteNotification: (notification: Notification) => void;
}

const typeStatusMap: Record<
  Notification["type"],
  "pending" | "completed" | "cancelled" | "failed"
> = {
  info: "pending",
  success: "completed",
  warning: "pending",
  error: "failed",
};

export function NotificationTable({
  notifications,
  onMarkAsRead,
  onDeleteNotification,
}: NotificationTableProps) {
  const columns = [
    {
      key: "title",
      header: "Notification",
      render: (notification: Notification) => (
        <div>
          <p className="font-medium">{notification.title}</p>
          <p className="text-sm text-muted-foreground">
            {notification.message}
          </p>
        </div>
      ),
    },
    {
      key: "type",
      header: "Type",
      render: (notification: Notification) => (
        <StatusBadge status={typeStatusMap[notification.type]} />
      ),
    },
    {
      key: "status",
      header: "Status",
      render: (notification: Notification) => (
        <span
          className={
            notification.status === "unread"
              ? "font-medium"
              : "text-muted-foreground"
          }
        >
          {notification.status === "unread" ? "Unread" : "Read"}
        </span>
      ),
    },
    {
      key: "createdAt",
      header: "Date",
      render: (notification: Notification) =>
        new Date(notification.createdAt).toLocaleString(),
    },
    {
      key: "action",
      header: "Action",
      render: (notification: Notification) =>
        notification.actionUrl ? (
          <Link href={notification.actionUrl}>
            <Button variant="ghost">View</Button>
          </Link>
        ) : null,
    },
    {
      key: "actions",
      header: "Actions",
      render: (notification: Notification) => (
        <div className="flex gap-2">
          {notification.status === "unread" ? (
            <Button
              variant="ghost"
              onClick={() => onMarkAsRead(notification)}
            >
              Mark Read
            </Button>
          ) : null}

          <Button
            variant="danger"
            onClick={() => onDeleteNotification(notification)}
          >
            Delete
          </Button>
        </div>
      ),
    },
  ];

  return (
    <Table
      columns={columns}
      data={notifications}
      getRowKey={(notification) => notification.id}
      emptyMessage="No notifications found."
    />
  );
}
