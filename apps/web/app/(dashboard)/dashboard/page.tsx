import { DashboardHeader } from "../../../components/dashboard/DashboardHeader";
import { KPIGrid } from "../../../components/dashboard/KPIGrid";
import { OrderPerformance } from "../../../components/dashboard/OrderPerformance";
import { QuickActions } from "../../../components/dashboard/QuickActions";
import { RecentActivity } from "../../../components/dashboard/RecentActivity";
import { RevenueOverview } from "../../../components/dashboard/RevenueOverview";
import {
  dashboardKPIs,
  orderSummary,
  quickActions,
  recentActivity,
  revenueData,
} from "../../../components/dashboard/data/dashboard-data";

export default function DashboardPage() {
  return (
    <div className="dashboard-page">
      <DashboardHeader
        title="Dashboard"
        description="Business overview and operational performance."
      />

      <KPIGrid kpis={dashboardKPIs} />

      <section className="dashboard-main-grid">
        <RevenueOverview data={revenueData} />
        <OrderPerformance summary={orderSummary} />
      </section>

      <section className="dashboard-secondary-grid">
        <RecentActivity activities={recentActivity} />
        <QuickActions actions={quickActions} />
      </section>
    </div>
  );
}
