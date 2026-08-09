import type { HTMLAttributes } from "react";

export type TrendIntent = "positive" | "negative" | "neutral" | "warning";

export interface TrendProps extends HTMLAttributes<HTMLDivElement> {
  value: string;
  label?: string;
  intent?: TrendIntent;
}

const trendSymbols: Record<TrendIntent, string> = {
  positive: "↑",
  negative: "↓",
  neutral: "→",
  warning: "!",
};

export function Trend({
  value,
  label,
  intent = "neutral",
  className = "",
  ...props
}: TrendProps) {
  return (
    <div
      className={`ui-trend ui-trend-${intent} ${className}`.trim()}
      {...props}
    >
      <span className="ui-trend-indicator" aria-hidden="true">
        {trendSymbols[intent]}
      </span>

      <span className="ui-trend-value">{value}</span>

      {label ? <span className="ui-trend-label">{label}</span> : null}
    </div>
  );
}
