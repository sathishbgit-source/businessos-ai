import { Button, Input } from "@/components/ui";
import type {
  BillingInterval,
  PlanStatus,
} from "./data/plan-data";

interface PlansHeaderProps {
  search: string;
  statusFilter: PlanStatus | "all";
  billingIntervalFilter: BillingInterval | "all";
  onSearchChange: (value: string) => void;
  onStatusFilterChange: (value: PlanStatus | "all") => void;
  onBillingIntervalFilterChange: (
    value: BillingInterval | "all",
  ) => void;
  onAddPlan: () => void;
}

export function PlansHeader({
  search,
  statusFilter,
  billingIntervalFilter,
  onSearchChange,
  onStatusFilterChange,
  onBillingIntervalFilterChange,
  onAddPlan,
}: PlansHeaderProps) {
  return (
    <section>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">
            Subscription Plans
          </h1>
          <p className="text-sm text-muted-foreground">
            Manage subscription plans, pricing, and billing intervals.
          </p>
        </div>

        <Button onClick={onAddPlan}>Add Plan</Button>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
        <div className="w-full sm:max-w-md">
          <Input
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Search plans..."
            aria-label="Search plans"
          />
        </div>

        <label className="flex flex-col gap-1 text-sm">
          <span>Status</span>
          <select
            value={statusFilter}
            onChange={(event) =>
              onStatusFilterChange(
                event.target.value as PlanStatus | "all",
              )
            }
            className="ui-input"
            aria-label="Filter plans by status"
          >
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="disabled">Disabled</option>
          </select>
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span>Billing Interval</span>
          <select
            value={billingIntervalFilter}
            onChange={(event) =>
              onBillingIntervalFilterChange(
                event.target.value as BillingInterval | "all",
              )
            }
            className="ui-input"
            aria-label="Filter plans by billing interval"
          >
            <option value="all">All</option>
            <option value="monthly">Monthly</option>
            <option value="yearly">Yearly</option>
          </select>
        </label>
      </div>
    </section>
  );
}
