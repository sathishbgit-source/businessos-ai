import { Button, Input } from "@/components/ui";
import type { InvoiceStatus } from "./data/invoice-data";

interface InvoiceHeaderProps {
  search: string;
  statusFilter: InvoiceStatus | "all";
  onSearchChange: (value: string) => void;
  onStatusFilterChange: (value: InvoiceStatus | "all") => void;
  onAddInvoice: () => void;
}

export function InvoiceHeader({
  search,
  statusFilter,
  onSearchChange,
  onStatusFilterChange,
  onAddInvoice,
}: InvoiceHeaderProps) {
  return (
    <section>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Invoices</h1>
          <p className="text-sm text-muted-foreground">
            Manage invoices, billing status, and payment due dates.
          </p>
        </div>

        <Button onClick={onAddInvoice}>Add Invoice</Button>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
        <div className="w-full sm:max-w-md">
          <Input
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Search invoices..."
            aria-label="Search invoices"
          />
        </div>

        <label className="flex flex-col gap-1 text-sm">
          <span>Status</span>
          <select
            value={statusFilter}
            onChange={(event) =>
              onStatusFilterChange(
                event.target.value as InvoiceStatus | "all",
              )
            }
            className="ui-input"
            aria-label="Filter invoices by status"
          >
            <option value="all">All</option>
            <option value="draft">Draft</option>
            <option value="sent">Sent</option>
            <option value="paid">Paid</option>
            <option value="overdue">Overdue</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </label>
      </div>
    </section>
  );
}
