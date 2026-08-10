export type SaleStatus =
  | "pending"
  | "completed"
  | "cancelled";

export interface Sale {
  id: string;
  saleNumber: string;
  customer: string;
  saleDate: string;
  amount: number;
  currency: string;
  status: SaleStatus;
}

export const salesData: Sale[] = [
  {
    id: "sale-001",
    saleNumber: "SALE-2026-001",
    customer: "ABC Tyres",
    saleDate: "2026-08-01",
    amount: 2450,
    currency: "AUD",
    status: "completed",
  },
  {
    id: "sale-002",
    saleNumber: "SALE-2026-002",
    customer: "Melbourne Auto Centre",
    saleDate: "2026-08-03",
    amount: 1850,
    currency: "AUD",
    status: "pending",
  },
  {
    id: "sale-003",
    saleNumber: "SALE-2026-003",
    customer: "Brisbane Fleet Services",
    saleDate: "2026-08-05",
    amount: 4200,
    currency: "AUD",
    status: "completed",
  },
  {
    id: "sale-004",
    saleNumber: "SALE-2026-004",
    customer: "Gold Coast Motors",
    saleDate: "2026-08-07",
    amount: 1250,
    currency: "AUD",
    status: "cancelled",
  },
];
