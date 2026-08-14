import { Button, Input } from "@/components/ui";
import type { BillingStatus } from "./data/billing-data";

interface BillingHeaderProps {
  search: string;
  statusFilter: BillingStatus | "all";
  onSearchChange: (value: string) => void;
  onStatusFilterChange: (value: BillingStatus | "all") => void;
  onAddBillingRecord: () => void;
}

export function BillingHeader({
  search,
  statusFilter,
  onSearchChange,
  onStatusFilterChange,
  onAddBillingRecord,
}: BillingHeaderProps) {
  return (
    <section>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Billing</h1>
          <p className="text-sm text-muted-foreground">
            Manage subscription billing records and billing periods.
          </p>
        </div>

        <Button onClick={onAddBillingRecord}>
          Add Billing Record
        </Button>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
        <div className="w-full sm:max-w-md">
          <Input
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Search billing records..."
            aria-label="Search billing records"
          />
        </div>

        <label className="flex flex-col gap-1 text-sm">
          <span>Status</span>
          <select
            value={statusFilter}
            onChange={(event) =>
              onStatusFilterChange(
                event.target.value as BillingStatus | "all",
              )
            }
            className="ui-input"
            aria-label="Filter billing records by status"
          >
            <option value="all">All</option>
            <option value="pending">Pending</option>
            <option value="billed">Billed</option>
            <option value="paid">Paid</option>
            <option value="failed">Failed</option>
          </select>
        </label>
      </div>
    </section>
  );
}
