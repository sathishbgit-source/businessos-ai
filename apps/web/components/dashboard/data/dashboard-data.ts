export interface DashboardKPI {
  label: string;
  value: string;
  change: string;
  detail: string;
  intent: "positive" | "negative" | "neutral" | "warning";
}

export interface RevenueDataPoint {
  month: string;
  value: number;
}

export interface OrderSummary {
  label: string;
  value: number;
}

export interface RecentActivity {
  title: string;
  description: string;
  time: string;
}

export const dashboardKPIs: DashboardKPI[] = [
  {
    label: "Total Revenue",
    value: "$128,450",
    change: "+12.5%",
    detail: "vs. previous month",
    intent: "positive",
  },
  {
    label: "Total Orders",
    value: "1,284",
    change: "+8.2%",
    detail: "vs. previous month",
    intent: "positive",
  },
  {
    label: "Active Customers",
    value: "642",
    change: "+5.4%",
    detail: "vs. previous month",
    intent: "positive",
  },
  {
    label: "Pending Orders",
    value: "38",
    change: "-4.1%",
    detail: "vs. previous month",
    intent: "positive",
  },
];

export const revenueData: RevenueDataPoint[] = [
  { month: "Jan", value: 48 },
  { month: "Feb", value: 64 },
  { month: "Mar", value: 52 },
  { month: "Apr", value: 76 },
  { month: "May", value: 61 },
  { month: "Jun", value: 84 },
  { month: "Jul", value: 72 },
  { month: "Aug", value: 92 },
  { month: "Sep", value: 68 },
  { month: "Oct", value: 80 },
  { month: "Nov", value: 74 },
  { month: "Dec", value: 96 },
];

export const orderSummary: OrderSummary[] = [
  { label: "Total orders", value: 1284 },
  { label: "Completed", value: 1146 },
  { label: "Pending", value: 38 },
  { label: "Processing", value: 100 },
];

export const recentActivity: RecentActivity[] = [
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

export const quickActions = [
  "Create Invoice",
  "Add Customer",
  "Add Product",
  "View Sales",
];
