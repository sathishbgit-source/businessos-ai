export type BillingStatus =
  | "pending"
  | "billed"
  | "paid"
  | "failed";

export interface BillingRecord {
  id: string;
  subscriptionId: string;
  customerId: string;
  planId: string;
  billingPeriodStart: string;
  billingPeriodEnd: string;
  amount: number;
  currency: string;
  status: BillingStatus;
}

export const billingData: BillingRecord[] = [
  {
    id: "BIL-001",
    subscriptionId: "SUB-001",
    customerId: "CUS-001",
    planId: "PLN-001",
    billingPeriodStart: "2026-08-01",
    billingPeriodEnd: "2026-08-31",
    amount: 29,
    currency: "AUD",
    status: "paid",
  },
  {
    id: "BIL-002",
    subscriptionId: "SUB-002",
    customerId: "CUS-002",
    planId: "PLN-002",
    billingPeriodStart: "2026-08-03",
    billingPeriodEnd: "2026-09-02",
    amount: 79,
    currency: "AUD",
    status: "billed",
  },
  {
    id: "BIL-003",
    subscriptionId: "SUB-003",
    customerId: "CUS-004",
    planId: "PLN-003",
    billingPeriodStart: "2026-08-05",
    billingPeriodEnd: "2027-08-04",
    amount: 199,
    currency: "AUD",
    status: "pending",
  },
  {
    id: "BIL-004",
    subscriptionId: "SUB-004",
    customerId: "CUS-003",
    planId: "PLN-001",
    billingPeriodStart: "2026-07-01",
    billingPeriodEnd: "2026-07-31",
    amount: 29,
    currency: "AUD",
    status: "failed",
  },
];
