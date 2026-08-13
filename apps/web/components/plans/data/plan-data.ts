export type BillingInterval = "monthly" | "yearly";

export type PlanStatus = "active" | "disabled";

export interface Plan {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  billingInterval: BillingInterval;
  features: string[];
  status: PlanStatus;
}

export const planData: Plan[] = [
  {
    id: "PLN-001",
    name: "Starter",
    description: "Essential tools for small businesses.",
    price: 29,
    currency: "AUD",
    billingInterval: "monthly",
    features: [
      "Core business management",
      "Product management",
      "Sales management",
    ],
    status: "active",
  },
  {
    id: "PLN-002",
    name: "Professional",
    description: "Advanced tools for growing businesses.",
    price: 79,
    currency: "AUD",
    billingInterval: "monthly",
    features: [
      "Everything in Starter",
      "Inventory management",
      "Payments management",
      "Advanced reporting",
    ],
    status: "active",
  },
  {
    id: "PLN-003",
    name: "Enterprise",
    description: "Full business operations for larger teams.",
    price: 199,
    currency: "AUD",
    billingInterval: "yearly",
    features: [
      "Everything in Professional",
      "Advanced controls",
      "Priority support",
      "Enterprise reporting",
    ],
    status: "active",
  },
  {
    id: "PLN-004",
    name: "Legacy",
    description: "Previously available subscription plan.",
    price: 49,
    currency: "AUD",
    billingInterval: "monthly",
    features: [
      "Core business management",
    ],
    status: "disabled",
  },
];
