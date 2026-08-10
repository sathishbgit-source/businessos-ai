import { Button, StatusBadge, Table } from "@/components/ui";
import type { Invoice } from "./data/invoice-data";

interface InvoiceTableProps {
  invoices: Invoice[];
  onEditInvoice: (invoice: Invoice) => void;
  onDeleteInvoice: (invoice: Invoice) => void;
}

export function InvoiceTable({
  invoices,
  onEditInvoice,
  onDeleteInvoice,
}: InvoiceTableProps) {
  const columns = [
    {
      key: "invoiceNumber",
      header: "Invoice",
      render: (invoice: Invoice) => (
        <div>
          <p className="font-medium">{invoice.invoiceNumber}</p>
          <p className="text-sm text-muted-foreground">{invoice.id}</p>
        </div>
      ),
    },
    {
      key: "customer",
      header: "Customer",
    },
    {
      key: "issueDate",
      header: "Issue Date",
    },
    {
      key: "dueDate",
      header: "Due Date",
    },
    {
      key: "amount",
      header: "Amount",
      render: (invoice: Invoice) =>
        `${invoice.currency} ${invoice.amount.toFixed(2)}`,
    },
    {
      key: "status",
      header: "Status",
      render: (invoice: Invoice) => {
        const statusMap = {
          draft: "pending",
          sent: "processing",
          paid: "completed",
          overdue: "warning",
          cancelled: "cancelled",
        } as const;

        return <StatusBadge status={statusMap[invoice.status]} />;
      },
    },
    {
      key: "actions",
      header: "Actions",
      render: (invoice: Invoice) => (
        <div className="flex gap-2">
          <Button
            variant="ghost"
            onClick={() => onEditInvoice(invoice)}
          >
            Edit
          </Button>
          <Button
            variant="danger"
            onClick={() => onDeleteInvoice(invoice)}
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
      data={invoices}
      getRowKey={(invoice) => invoice.id}
      emptyMessage="No invoices found."
    />
  );
}
