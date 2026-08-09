import { Button, StatusBadge, Table } from "@/components/ui";
import type { Customer } from "./data/customer-data";

interface CustomerTableProps {
  customers: Customer[];
}

export function CustomerTable({ customers }: CustomerTableProps) {
  const columns = [
    {
      key: "name",
      header: "Name",
      render: (customer: Customer) => (
        <div>
          <div className="font-medium">{customer.name}</div>
          <div className="text-sm text-muted-foreground">{customer.id}</div>
        </div>
      ),
    },
    {
      key: "company",
      header: "Company",
    },
    {
      key: "email",
      header: "Email",
    },
    {
      key: "phone",
      header: "Phone",
    },
    {
      key: "status",
      header: "Status",
      render: (customer: Customer) => (
        <StatusBadge status={customer.status} />
      ),
    },
    {
      key: "actions",
      header: "Actions",
      render: () => (
        <Button variant="ghost">
          View
        </Button>
      ),
    },
  ];

  return (
    <Table
      columns={columns}
      data={customers}
      getRowKey={(customer) => customer.id}
      emptyMessage="No customers found."
    />
  );
}
