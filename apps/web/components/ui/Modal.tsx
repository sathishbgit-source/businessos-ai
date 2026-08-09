import type { ReactNode } from "react";

export interface ModalProps {
  open: boolean;
  title?: string;
  children: ReactNode;
  onClose: () => void;
}

export function Modal({ open, title, children, onClose }: ModalProps) {
  if (!open) {
    return null;
  }

  return (
    <div className="ui-modal-backdrop" role="presentation" onMouseDown={onClose}>
      <div
        className="ui-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? "ui-modal-title" : undefined}
        onMouseDown={(event) => event.stopPropagation()}
      >
        <div className="ui-modal-header">
          {title ? (
            <h2 id="ui-modal-title" className="ui-modal-title">
              {title}
            </h2>
          ) : null}

          <button
            type="button"
            className="ui-modal-close"
            aria-label="Close modal"
            onClick={onClose}
          >
            ×
          </button>
        </div>

       <div className="ui-modal-content">{children}</div>
      </div>
    </div>
  );
}
