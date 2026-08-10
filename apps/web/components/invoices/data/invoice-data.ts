export type InvoiceStatus =
  | "draft"
  | "sent"
  | "paid"
  | "overdue"
  | "cancelled";

export interface Invoice {
  id: string;
  invoiceNumber: string;
  customer: string;
  issueDate: string;
  dueDate: string;
  amount: number;
  status: InvoiceStatus;
  currency: string;
}

export const invoiceData: Invoice[] = [
  {
    id: "INV-001",
    invoiceNumber: "INV-2026-001",
    customer: "Smith Automotive",
    issueDate: "2026-08-01",
    dueDate: "2026-08-15",
    amount: 2450,
    status: "paid",
    currency: "AUD",
  },
  {
    id: "INV-002",
    invoiceNumber: "INV-2026-002",
    customer: "Brown Motors",
    issueDate: "2026-08-03",
    dueDate: "2026-08-17",
    amount: 3180,
    status: "sent",
    currency: "AUD",
  },
  {
    id: "INV-003",
    invoiceNumber: "INV-2026-003",
    customer: "Wilson Fleet Services",
    issueDate: "2026-08-04",
    dueDate: "2026-08-18",
    amount: 5620,
    status: "overdue",
    currency: "AUD",
  },
  {
    id: "INV-004",
    invoiceNumber: "INV-2026-004",
    customer: "Taylor Auto Group",
    issueDate: "2026-08-06",
    dueDate: "2026-08-20",
    amount: 1875,
    status: "draft",
    currency: "AUD",
  },
  {
    id: "INV-005",
    invoiceNumber: "INV-2026-005",
    customer: "Anderson Logistics",
    issueDate: "2026-08-07",
    dueDate: "2026-08-21",
    amount: 4290,
    status: "cancelled",
    currency: "AUD",
  },
];
