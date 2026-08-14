import { Button, StatusBadge, Table } from "@/components/ui";
import type { BillingRecord } from "./data/billing-data";

interface BillingTableProps {
  billingRecords: BillingRecord[];
  onEditBillingRecord: (record: BillingRecord) => void;
  onDeleteBillingRecord: (record: BillingRecord) => void;
}

export function BillingTable({
  billingRecords,
  onEditBillingRecord,
  onDeleteBillingRecord,
}: BillingTableProps) {
  const columns = [
    {
      key: "id",
      header: "Billing",
      render: (record: BillingRecord) => (
        <div>
          <p className="font-medium">{record.id}</p>
          <p className="text-sm text-muted-foreground">
            {record.subscriptionId}
          </p>
        </div>
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
      key: "billingPeriod",
      header: "Billing Period",
      render: (record: BillingRecord) =>
        `${record.billingPeriodStart} → ${record.billingPeriodEnd}`,
    },
    {
      key: "amount",
      header: "Amount",
      render: (record: BillingRecord) =>
        `${record.currency} ${record.amount.toFixed(2)}`,
    },
    {
      key: "status",
      header: "Status",
      render: (record: BillingRecord) => {
        const statusMap = {
          pending: "pending",
          billed: "processing",
          paid: "completed",
          failed: "failed",
        } as const;

        return (
          <StatusBadge status={statusMap[record.status]} />
        );
      },
    },
    {
      key: "actions",
      header: "Actions",
      render: (record: BillingRecord) => (
        <div className="flex gap-2">
          <Button
            variant="ghost"
            onClick={() => onEditBillingRecord(record)}
          >
            Edit
          </Button>

          <Button
            variant="danger"
            onClick={() => onDeleteBillingRecord(record)}
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
      data={billingRecords}
      getRowKey={(record) => record.id}
      emptyMessage="No billing records found."
    />
  );
}
