export interface LoadingProps {
  label?: string;
}

export function Loading({ label = "Loading..." }: LoadingProps) {
  return (
    <div className="ui-loading" role="status" aria-live="polite">
      <span className="ui-spinner" aria-hidden="true" />
      <span>{label}</span>
    </div>
  );
}
