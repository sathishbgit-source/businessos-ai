import { Card } from "../ui";
import type { RevenueDataPoint } from "./data/dashboard-data";

interface RevenueOverviewProps {
  data: RevenueDataPoint[];
}

export function RevenueOverview({ data }: RevenueOverviewProps) {
  return (
    <Card
      title="Revenue Overview"
      description="Revenue performance for the current period."
    >
      <div className="dashboard-chart-placeholder">
        <div className="dashboard-chart-bars" aria-hidden="true">
          {data.map((point) => (
            <div
              key={point.month}
              className="dashboard-chart-bar"
              style={{ height: `${point.value}%` }}
            />
          ))}
        </div>

        <div className="dashboard-chart-labels">
          {data.map((point) => (
            <span key={point.month}>{point.month}</span>
          ))}
        </div>
      </div>
    </Card>
  );
}
