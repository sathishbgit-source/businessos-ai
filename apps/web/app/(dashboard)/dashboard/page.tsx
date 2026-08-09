import { Card } from "../../../components/ui";

const kpis = [
  {
    label: "Total Revenue",
    value: "$128,450",
    change: "+12.5%",
    detail: "vs. previous month",
  },
  {
    label: "Total Orders",
    value: "1,284",
    change: "+8.2%",
    detail: "vs. previous month",
  },
  {
    label: "Active Customers",
    value: "642",
    change: "+5.4%",
    detail: "vs. previous month",
  },
  {
    label: "Pending Orders",
    value: "38",
    change: "-4.1%",
    detail: "vs. previous month",
  },
];

const recentActivity = [
  {
    title: "New order received",
    description: "Order #ORD-1048 was placed by Acme Logistics.",
    time: "10 minutes ago",
  },
  {
    title: "Invoice generated",
    description: "Invoice #INV-2031 was generated successfully.",
    time: "32 minutes ago",
  },
  {
    title: "Customer added",
    description: "Northstar Motors was added to your customer list.",
    time: "1 hour ago",
  },
  {
    title: "Payment received",
    description: "Payment of $4,850 was received for invoice #INV-2027.",
    time: "2 hours ago",
  },
];

const quickActions = [
  "Create Invoice",
  "Add Customer",
  "Add Product",
  "View Sales",
];

export default function DashboardPage() {
  return (
    <div className="dashboard-page">
      <header className="dashboard-header">
        <div>
          <h2>Dashboard</h2>
          <p>Business overview and operational performance.</p>
        </div>
      </header>

      <section className="dashboard-kpi-grid" aria-label="Key performance indicators">
        {kpis.map((kpi) => (
          <Card key={kpi.label} className="dashboard-kpi-card">
            <p className="dashboard-kpi-label">{kpi.label}</p>
            <p className="dashboard-kpi-value">{kpi.value}</p>
            <p className="dashboard-kpi-change">
              <span>{kpi.change}</span> {kpi.detail}
            </p>
          </Card>
        ))}
      </section>

      <section className="dashboard-main-grid">
        <Card
          title="Revenue Overview"
          description="Revenue performance for the current period."
        >
          <div className="dashboard-chart-placeholder">
            <div className="dashboard-chart-bars" aria-hidden="true">
              {[48, 64, 52, 76, 61, 84, 72, 92, 68, 80, 74, 96].map(
                (height, index) => (
                  <div
                    key={index}
                    className="dashboard-chart-bar"
                    style={{ height: `${height}%` }}
                  />
                ),
              )}
            </div>

            <div className="dashboard-chart-labels">
              <span>Jan</span>
              <span>Feb</span>
              <span>Mar</span>
              <span>Apr</span>
              <span>May</span>
              <span>Jun</span>
            </div>
          </div>
        </Card>

        <Card
          title="Order Performance"
          description="Current order status distribution."
        >
          <div className="dashboard-order-summary">
            <div>
              <strong>1,284</strong>
              <span>Total orders</span>
            </div>
            <div>
              <strong>1,146</strong>
              <span>Completed</span>
            </div>
            <div>
              <strong>38</strong>
              <span>Pending</span>
            </div>
            <div>
              <strong>100</strong>
              <span>Processing</span>
            </div>
          </div>
        </Card>
      </section>

      <section className="dashboard-secondary-grid">
        <Card
          title="Recent Activity"
          description="Latest activity across your business."
        >
          <div className="dashboard-activity-list">
            {recentActivity.map((activity) => (
              <div key={activity.title} className="dashboard-activity-item">
                <div>
                  <strong>{activity.title}</strong>
                  <p>{activity.description}</p>
                </div>
                <time>{activity.time}</time>
              </div>
            ))}
          </div>
        </Card>

        <Card
          title="Quick Actions"
          description="Common actions to manage your business."
        >
          <div className="dashboard-actions">
            {quickActions.map((action) => (
              <button key={action} type="button" className="dashboard-action">
                {action}
              </button>
            ))}
          </div>
        </Card>
      </section>
    </div>
  );
}
