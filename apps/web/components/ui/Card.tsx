import type { HTMLAttributes, ReactNode } from "react";

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  title?: string;
  description?: string;
  children: ReactNode;
}

export function Card({
  title,
  description,
  children,
  className = "",
  ...props
}: CardProps) {
  return (
    <section className={`ui-card ${className}`.trim()} {...props}>
      {title ? <h2 className="ui-card-title">{title}</h2> : null}
      {description ? (
        <p className="ui-card-description">{description}</p>
      ) : null}
      <div className="ui-card-content">{children}</div>
    </section>
  );
}
