import { Button, StatusBadge, Table } from "@/components/ui";
import type { Subscription } from "./data/subscription-data";

interface SubscriptionTableProps {
  subscriptions: Subscription[];
  onEditSubscription: (subscription: Subscription) => void;
  onDeleteSubscription: (subscription: Subscription) => void;
}

export function SubscriptionTable({
  subscriptions,
  onEditSubscription,
  onDeleteSubscription,
}: SubscriptionTableProps) {
  const columns = [
    {
      key: "id",
      header: "Subscription",
      render: (subscription: Subscription) => (
        <p className="font-medium">{subscription.id}</p>
      ),
    },
    {
      key: "customerId",
      header: "Customer",
    },
    {
      key: "planId",
      header: "Plan",
    },
    {
      key: "startDate",
      header: "Start Date",
    },
    {
      key: "currentPeriod",
      header: "Current Period",
      render: (subscription: Subscription) =>
        `${subscription.currentPeriodStart} → ${subscription.currentPeriodEnd}`,
    },
    {
      key: "status",
      header: "Status",
      render: (subscription: Subscription) => (
        <StatusBadge status={subscription.status} />
      ),
    },
    {
      key: "actions",
      header: "Actions",
      render: (subscription: Subscription) => (
        <div className="flex gap-2">
          <Button
            variant="ghost"
            onClick={() => onEditSubscription(subscription)}
          >
            Edit
          </Button>

          <Button
            variant="danger"
            onClick={() => onDeleteSubscription(subscription)}
          >
            Delete
          </Button>
        </div>
      ),
    },
  ];

  return (
    <Table
      columns={columns}
      data={subscriptions}
      getRowKey={(subscription) => subscription.id}
      emptyMessage="No subscriptions found."
    />
  );
}
