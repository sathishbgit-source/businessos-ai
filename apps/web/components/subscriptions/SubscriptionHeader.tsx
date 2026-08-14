import { Button, Input } from "@/components/ui";
import type { SubscriptionStatus } from "./data/subscription-data";

interface SubscriptionHeaderProps {
  search: string;
  statusFilter: SubscriptionStatus | "all";
  onSearchChange: (value: string) => void;
  onStatusFilterChange: (value: SubscriptionStatus | "all") => void;
  onAddSubscription: () => void;
}

export function SubscriptionHeader({
  search,
  statusFilter,
  onSearchChange,
  onStatusFilterChange,
  onAddSubscription,
}: SubscriptionHeaderProps) {
  return (
    <section>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Subscriptions</h1>
          <p className="text-sm text-muted-foreground">
            Manage customer subscriptions and plan assignments.
          </p>
        </div>

        <Button onClick={onAddSubscription}>
          Add Subscription
        </Button>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
        <div className="w-full sm:max-w-md">
          <Input
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Search subscriptions..."
            aria-label="Search subscriptions"
          />
        </div>

        <label className="flex flex-col gap-1 text-sm">
          <span>Status</span>
          <select
            value={statusFilter}
            onChange={(event) =>
              onStatusFilterChange(
                event.target.value as SubscriptionStatus | "all",
              )
            }
            className="ui-input"
            aria-label="Filter subscriptions by status"
          >
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </label>
      </div>
    </section>
  );
}
