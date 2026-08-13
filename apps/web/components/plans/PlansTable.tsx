import { Button, StatusBadge, Table } from "@/components/ui";
import type { Plan } from "./data/plan-data";

interface PlansTableProps {
  plans: Plan[];
  onEditPlan: (plan: Plan) => void;
  onDeletePlan: (plan: Plan) => void;
}

export function PlansTable({
  plans,
  onEditPlan,
  onDeletePlan,
}: PlansTableProps) {
  const columns = [
    {
      key: "name",
      header: "Plan",
      render: (plan: Plan) => (
        <div>
          <p className="font-medium">{plan.name}</p>
          <p className="text-sm text-muted-foreground">
            {plan.description}
          </p>
        </div>
      ),
    },
    {
      key: "price",
      header: "Price",
      render: (plan: Plan) =>
        `${plan.currency} ${plan.price.toFixed(2)}`,
    },
    {
      key: "billingInterval",
      header: "Billing",
      render: (plan: Plan) =>
        plan.billingInterval === "monthly" ? "Monthly" : "Yearly",
    },
    {
      key: "features",
      header: "Features",
      render: (plan: Plan) => plan.features.length,
    },
    {
      key: "status",
      header: "Status",
      render: (plan: Plan) => (
        <StatusBadge status={plan.status} />
      ),
    },
    {
      key: "actions",
      header: "Actions",
      render: (plan: Plan) => (
        <div className="flex gap-2">
          <Button
            variant="ghost"
            onClick={() => onEditPlan(plan)}
          >
            Edit
          </Button>
          <Button
            variant="danger"
            onClick={() => onDeletePlan(plan)}
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
      data={plans}
      getRowKey={(plan) => plan.id}
      emptyMessage="No subscription plans found."
    />
  );
}
