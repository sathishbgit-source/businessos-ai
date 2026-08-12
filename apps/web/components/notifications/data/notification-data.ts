export type NotificationType =
  | "info"
  | "success"
  | "warning"
  | "error";

export type NotificationStatus =
  | "unread"
  | "read";

export interface Notification {
  id: string;
  title: string;
  message: string;
  type: NotificationType;
  status: NotificationStatus;
  createdAt: string;
  actionUrl?: string;
}

export const notificationData: Notification[] = [
  {
    id: "NOT-001",
    title: "Payment Received",
    message: "Payment PAY-2026-001 has been completed successfully.",
    type: "success",
    status: "unread",
    createdAt: "2026-08-10T09:15:00",
    actionUrl: "/payments",
  },
  {
    id: "NOT-002",
    title: "Invoice Due",
    message: "Invoice INV-2026-002 is approaching its due date.",
    type: "warning",
    status: "unread",
    createdAt: "2026-08-10T08:30:00",
    actionUrl: "/invoices",
  },
  {
    id: "NOT-003",
    title: "New Customer Added",
    message: "Melbourne Auto Centre was added to your customers.",
    type: "info",
    status: "read",
    createdAt: "2026-08-09T16:45:00",
    actionUrl: "/customers",
  },
  {
    id: "NOT-004",
    title: "Payment Failed",
    message: "Payment PAY-2026-004 failed and requires attention.",
    type: "error",
    status: "unread",
    createdAt: "2026-08-09T14:20:00",
    actionUrl: "/payments",
  },
  {
    id: "NOT-005",
    title: "Product Stock Updated",
    message: "Product inventory has been updated successfully.",
    type: "success",
    status: "read",
    createdAt: "2026-08-08T11:10:00",
    actionUrl: "/products",
  },
];
