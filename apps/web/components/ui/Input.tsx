import type { InputHTMLAttributes } from "react";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export function Input({ label, error, id, ...props }: InputProps) {
  return (
    <div className="ui-field">
      {label ? (
        <label className="ui-label" htmlFor={id}>
          {label}
        </label>
      ) : null}

      <input
        id={id}
        className={`ui-input${error ? " ui-input-error" : ""}`}
        {...props}
      />

      {error ? <p className="ui-error-text">{error}</p> : null}
    </div>
  );
}
