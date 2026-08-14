export type SubscriptionStatus = "active" | "cancelled";

export interface Subscription {
  id: string;
  customerId: string;
  planId: string;
  status: SubscriptionStatus;
  startDate: string;
  currentPeriodStart: string;
  currentPeriodEnd: string;
  createdAt: string;
}

export const subscriptionData: Subscription[] = [
  {
    id: "SUB-001",
    customerId: "CUS-001",
    planId: "PLN-001",
    status: "active",
    startDate: "2026-08-01",
    currentPeriodStart: "2026-08-01",
    currentPeriodEnd: "2026-08-31",
    createdAt: "2026-08-01",
  },
  {
    id: "SUB-002",
    customerId: "CUS-002",
    planId: "PLN-002",
    status: "active",
    startDate: "2026-08-03",
    currentPeriodStart: "2026-08-03",
    currentPeriodEnd: "2026-09-02",
    createdAt: "2026-08-03",
  },
  {
    id: "SUB-003",
    customerId: "CUS-004",
    planId: "PLN-003",
    status: "active",
    startDate: "2026-08-05",
    currentPeriodStart: "2026-08-05",
    currentPeriodEnd: "2027-08-04",
    createdAt: "2026-08-05",
  },
  {
    id: "SUB-004",
    customerId: "CUS-003",
    planId: "PLN-001",
    status: "cancelled",
    startDate: "2026-07-01",
    currentPeriodStart: "2026-07-01",
    currentPeriodEnd: "2026-07-31",
    createdAt: "2026-07-01",
  },
];
