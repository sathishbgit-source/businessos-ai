import type { HTMLAttributes, ReactNode } from "react";

type BadgeVariant = "default" | "success" | "warning" | "danger" | "info";

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
  children: ReactNode;
}

export function Badge({
  children,
  variant = "default",
  className = "",
  ...props
}: BadgeProps) {
  return (
    <span
      className={`ui-badge ui-badge-${variant} ${className}`.trim()}
      {...props}
    >
      {children}
    </span>
  );
}
