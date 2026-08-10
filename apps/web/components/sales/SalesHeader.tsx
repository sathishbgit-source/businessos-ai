"use client";

import { Button, Input, Select } from "@/components/ui";
import type { SaleStatus } from "@/components/sales/data/sales-data";

interface SalesHeaderProps {
  search: string;
  statusFilter: SaleStatus | "all";
  onSearchChange: (value: string) => void;
  onStatusFilterChange: (value: SaleStatus | "all") => void;
  onAddSale: () => void;
}

const statusOptions = [
  { value: "all", label: "All Statuses" },
  { value: "pending", label: "Pending" },
  { value: "completed", label: "Completed" },
  { value: "cancelled", label: "Cancelled" },
];

export function SalesHeader({
  search,
  statusFilter,
  onSearchChange,
  onStatusFilterChange,
  onAddSale,
}: SalesHeaderProps) {
  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
      <div className="flex flex-1 flex-col gap-4 md:flex-row">
        <Input
          label="Search"
          value={search}
          placeholder="Search sales..."
          onChange={(event) => onSearchChange(event.target.value)}
        />

        <Select
          label="Status"
          value={statusFilter}
          options={statusOptions}
          onChange={(event) =>
            onStatusFilterChange(event.target.value as SaleStatus | "all")
          }
        />
      </div>

      <Button type="button" onClick={onAddSale}>
        Add Sale
      </Button>
    </div>
  );
}
