import type { ReactNode } from "react";

type ToastVariant = "success" | "error" | "warning" | "info";

export interface ToastProps {
  message: ReactNode;
  variant?: ToastVariant;
  onClose?: () => void;
}

export function Toast({
  message,
  variant = "info",
  onClose,
}: ToastProps) {
  return (
    <div
      className={`ui-toast ui-toast-${variant}`}
      role={variant === "error" ? "alert" : "status"}
    >
      <span>{message}</span>

      {onClose ? (
        <button
          type="button"
          className="ui-toast-close"
          aria-label="Close notification"
          onClick={onClose}
        >
          ×
        </button>
      ) : null}
    </div>
  );
}
