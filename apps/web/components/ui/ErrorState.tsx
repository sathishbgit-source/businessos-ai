import type { ReactNode } from "react";

export interface ErrorStateProps {
  title?: string;
  message?: ReactNode;
  action?: ReactNode;
}

export function ErrorState({
  title = "Something went wrong",
  message = "We couldn't complete this request.",
  action,
}: ErrorStateProps) {
  return (
    <div className="ui-error-state" role="alert">
      <h2>{title}</h2>
      <p>{message}</p>
      {action ? <div className="ui-error-action">{action}</div> : null}
    </div>
  );
}
