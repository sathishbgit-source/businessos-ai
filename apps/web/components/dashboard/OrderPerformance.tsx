import { Card } from "../ui";
import type { OrderSummary } from "./data/dashboard-data";

interface OrderPerformanceProps {
  summary: OrderSummary[];
}

export function OrderPerformance({
  summary,
}: OrderPerformanceProps) {
  return (
    <Card
      title="Order Performance"
      description="Current order status distribution."
    >
      <div className="dashboard-order-summary">
        {summary.map((item) => (
          <div key={item.label}>
            <strong>{item.value.toLocaleString()}</strong>
            <span>{item.label}</span>
          </div>
        ))}
      </div>
    </Card>
  );
}
