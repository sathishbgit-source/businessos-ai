"use client";

import { StatusBadge, Table } from "@/components/ui";
import type { Payment } from "@/components/payments/data/payment-data";

interface PaymentTableProps {
  payments: Payment[];
  onEditPayment: (payment: Payment) => void;
  onDeletePayment: (payment: Payment) => void;
}

const methodLabels: Record<Payment["method"], string> = {
  card: "Card",
  bank_transfer: "Bank Transfer",
  cash: "Cash",
  other: "Other",
};

const statusMap: Record<
  Payment["status"],
  "pending" | "completed" | "failed" | "cancelled"
> = {
  pending: "pending",
  completed: "completed",
  failed: "failed",
  refunded: "cancelled",
  cancelled: "cancelled",
};

export function PaymentTable({
  payments,
  onEditPayment,
  onDeletePayment,
}: PaymentTableProps) {
  const columns = [
    {
      key: "paymentNumber",
      header: "Payment",
    },
    {
      key: "customer",
      header: "Customer",
    },
    {
      key: "paymentDate",
      header: "Date",
    },
    {
      key: "amount",
      header: "Amount",
      render: (payment: Payment) =>
        `${payment.currency} ${payment.amount.toLocaleString()}`,
    },
    {
      key: "method",
      header: "Method",
      render: (payment: Payment) => methodLabels[payment.method],
    },
    {
      key: "status",
      header: "Status",
      render: (payment: Payment) => (
        <StatusBadge status={statusMap[payment.status]} />
      ),
    },
    {
      key: "actions",
      header: "Actions",
      render: (payment: Payment) => (
        <div className="flex gap-2">
          <button type="button" onClick={() => onEditPayment(payment)}>
            Edit
          </button>
          <button type="button" onClick={() => onDeletePayment(payment)}>
            Delete
          </button>
        </div>
      ),
    },
  ];

  return (
    <Table
      columns={columns}
      data={payments}
      getRowKey={(payment) => payment.id}
      emptyMessage="No payments found."
    />
  );
}
