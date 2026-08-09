import type { HTMLAttributes } from "react";

export type Status =
  | "active"
  | "pending"
  | "completed"
  | "failed"
  | "warning"
  | "disabled"
  | "processing"
  | "cancelled";

export interface StatusBadgeProps extends HTMLAttributes<HTMLSpanElement> {
  status: Status;
}

const statusLabels: Record<Status, string> = {
  active: "Active",
  pending: "Pending",
  completed: "Completed",
  failed: "Failed",
  warning: "Warning",
  disabled: "Disabled",
  processing: "Processing",
  cancelled: "Cancelled",
};

const statusVariants: Record<Status, string> = {
  active: "success",
  pending: "warning",
  completed: "success",
  failed: "danger",
  warning: "warning",
  disabled: "neutral",
  processing: "info",
  cancelled: "neutral",
};

export function StatusBadge({
  status,
  className = "",
  ...props
}: StatusBadgeProps) {
  const variant = statusVariants[status];

  return (
    <span
      className={`ui-status-badge ui-status-badge-${variant} ${className}`.trim()}
      {...props}
    >
      <span className="ui-status-badge-dot" aria-hidden="true" />
      <span>{statusLabels[status]}</span>
    </span>
  );
}
