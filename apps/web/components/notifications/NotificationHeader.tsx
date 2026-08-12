"use client";

import { Button, Input, Select } from "@/components/ui";
import type {
  NotificationStatus,
  NotificationType,
} from "@/components/notifications/data/notification-data";

interface NotificationHeaderProps {
  search: string;
  typeFilter: NotificationType | "all";
  statusFilter: NotificationStatus | "all";
  onSearchChange: (value: string) => void;
  onTypeFilterChange: (value: NotificationType | "all") => void;
  onStatusFilterChange: (value: NotificationStatus | "all") => void;
  onMarkAllAsRead: () => void;
}

const typeOptions = [
  { value: "all", label: "All Types" },
  { value: "info", label: "Info" },
  { value: "success", label: "Success" },
  { value: "warning", label: "Warning" },
  { value: "error", label: "Error" },
];

const statusOptions = [
  { value: "all", label: "All Notifications" },
  { value: "unread", label: "Unread" },
  { value: "read", label: "Read" },
];

export function NotificationHeader({
  search,
  typeFilter,
  statusFilter,
  onSearchChange,
  onTypeFilterChange,
  onStatusFilterChange,
  onMarkAllAsRead,
}: NotificationHeaderProps) {
  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Notifications</h1>
          <p className="text-sm text-muted-foreground">
            View and manage your notifications.
          </p>
        </div>

        <Button type="button" onClick={onMarkAllAsRead}>
          Mark All as Read
        </Button>
      </div>

      <div className="flex flex-col gap-4 md:flex-row">
        <Input
          label="Search"
          value={search}
          placeholder="Search notifications..."
          onChange={(event) => onSearchChange(event.target.value)}
        />

        <Select
          label="Type"
          value={typeFilter}
          options={typeOptions}
          onChange={(event) =>
            onTypeFilterChange(
              event.target.value as NotificationType | "all",
            )
          }
        />

        <Select
          label="Status"
          value={statusFilter}
          options={statusOptions}
          onChange={(event) =>
            onStatusFilterChange(
              event.target.value as NotificationStatus | "all",
            )
          }
        />
      </div>
    </div>
  );
}
