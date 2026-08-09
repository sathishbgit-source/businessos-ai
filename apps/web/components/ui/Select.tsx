import type { SelectHTMLAttributes } from "react";

export interface SelectOption {
  label: string;
  value: string;
}

export interface SelectProps
  extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  options: SelectOption[];
}

export function Select({
  label,
  error,
  id,
  options,
  ...props
}: SelectProps) {
  return (
    <div className="ui-field">
      {label ? (
        <label className="ui-label" htmlFor={id}>
          {label}
        </label>
      ) : null}

      <select
        id={id}
        className={`ui-select${error ? " ui-input-error" : ""}`}
        {...props}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>

      {error ? <p className="ui-error-text">{error}</p> : null}
    </div>
  );
}
