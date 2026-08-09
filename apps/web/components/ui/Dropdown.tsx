import type { ReactNode } from "react";

export interface DropdownItem {
  label: string;
  value: string;
  disabled?: boolean;
}

export interface DropdownProps {
  label: ReactNode;
  items: DropdownItem[];
  onSelect: (value: string) => void;
}

export function Dropdown({ label, items, onSelect }: DropdownProps) {
  return (
    <details className="ui-dropdown">
      <summary className="ui-dropdown-trigger">{label}</summary>

      <div className="ui-dropdown-menu" role="menu">
        {items.map((item) => (
          <button
            key={item.value}
            type="button"
            className="ui-dropdown-item"
            disabled={item.disabled}
            role="menuitem"
            onClick={() => onSelect(item.value)}
          >
            {item.label}
          </button>
        ))}
      </div>
    </details>
  );
}
