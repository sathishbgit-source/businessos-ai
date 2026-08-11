"use client";

import { Button, Input, Select } from "@/components/ui";
import type {
  PaymentMethod,
  PaymentStatus,
} from "@/components/payments/data/payment-data";

interface PaymentHeaderProps {
  search: string;
  statusFilter: PaymentStatus | "all";
  methodFilter: PaymentMethod | "all";
  onSearchChange: (value: string) => void;
  onStatusFilterChange: (value: PaymentStatus | "all") => void;
  onMethodFilterChange: (value: PaymentMethod | "all") => void;
  onAddPayment: () => void;
}

const statusOptions = [
  { value: "all", label: "All Statuses" },
  { value: "pending", label: "Pending" },
  { value: "completed", label: "Completed" },
  { value: "failed", label: "Failed" },
  { value: "refunded", label: "Refunded" },
  { value: "cancelled", label: "Cancelled" },
];

const methodOptions = [
  { value: "all", label: "All Methods" },
  { value: "card", label: "Card" },
  { value: "bank_transfer", label: "Bank Transfer" },
  { value: "cash", label: "Cash" },
  { value: "other", label: "Other" },
];

export function PaymentHeader({
  search,
  statusFilter,
  methodFilter,
  onSearchChange,
  onStatusFilterChange,
  onMethodFilterChange,
  onAddPayment,
}: PaymentHeaderProps) {
  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
      <div className="flex flex-1 flex-col gap-4 md:flex-row">
        <Input
          label="Search"
          value={search}
          placeholder="Search payments..."
          onChange={(event) => onSearchChange(event.target.value)}
        />

        <Select
          label="Status"
          value={statusFilter}
          options={statusOptions}
          onChange={(event) =>
            onStatusFilterChange(
              event.target.value as PaymentStatus | "all",
            )
          }
        />

        <Select
          label="Method"
          value={methodFilter}
          options={methodOptions}
          onChange={(event) =>
            onMethodFilterChange(
              event.target.value as PaymentMethod | "all",
            )
          }
        />
      </div>

      <Button type="button" onClick={onAddPayment}>
        Add Payment
      </Button>
    </div>
  );
}
