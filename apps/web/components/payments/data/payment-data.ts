export type PaymentStatus =
  | "pending"
  | "completed"
  | "failed"
  | "refunded"
  | "cancelled";

export type PaymentMethod =
  | "card"
  | "bank_transfer"
  | "cash"
  | "other";

export interface Payment {
  id: string;
  paymentNumber: string;
  customer: string;
  paymentDate: string;
  amount: number;
  currency: string;
  method: PaymentMethod;
  status: PaymentStatus;
}

export const paymentData: Payment[] = [
  {
    id: "PAY-001",
    paymentNumber: "PAY-2026-001",
    customer: "Smith Automotive",
    paymentDate: "2026-08-01",
    amount: 2450,
    currency: "AUD",
    method: "bank_transfer",
    status: "completed",
  },
  {
    id: "PAY-002",
    paymentNumber: "PAY-2026-002",
    customer: "Brown Motors",
    paymentDate: "2026-08-03",
    amount: 3180,
    currency: "AUD",
    method: "card",
    status: "pending",
  },
  {
    id: "PAY-003",
    paymentNumber: "PAY-2026-003",
    customer: "Wilson Fleet Services",
    paymentDate: "2026-08-05",
    amount: 5620,
    currency: "AUD",
    method: "bank_transfer",
    status: "completed",
  },
  {
    id: "PAY-004",
    paymentNumber: "PAY-2026-004",
    customer: "Taylor Auto Group",
    paymentDate: "2026-08-07",
    amount: 1875,
    currency: "AUD",
    method: "cash",
    status: "failed",
  },
  {
    id: "PAY-005",
    paymentNumber: "PAY-2026-005",
    customer: "Anderson Logistics",
    paymentDate: "2026-08-09",
    amount: 4290,
    currency: "AUD",
    method: "card",
    status: "refunded",
  },
];
