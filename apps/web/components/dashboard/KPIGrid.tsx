import { Card, Trend } from "../ui";
import type { DashboardKPI } from "./data/dashboard-data";

interface KPIGridProps {
  kpis: DashboardKPI[];
}

export function KPIGrid({ kpis }: KPIGridProps) {
  return (
    <section
      className="dashboard-kpi-grid"
      aria-label="Key performance indicators"
    >
      {kpis.map((kpi) => (
        <Card key={kpi.label} className="dashboard-kpi-card">
          <p className="dashboard-kpi-label">{kpi.label}</p>
          <p className="dashboard-kpi-value">{kpi.value}</p>

          <div className="dashboard-kpi-change">
            <Trend
              value={kpi.change}
              label={kpi.detail}
              intent={kpi.intent}
            />
          </div>
        </Card>
      ))}
    </section>
  );
}
