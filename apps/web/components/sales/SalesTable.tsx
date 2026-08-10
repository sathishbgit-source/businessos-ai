"use client";

import { StatusBadge, Table } from "@/components/ui";
import type { Sale } from "@/components/sales/data/sales-data";

interface SalesTableProps {
  sales: Sale[];
  onEditSale: (sale: Sale) => void;
  onDeleteSale: (sale: Sale) => void;
}

export function SalesTable({
  sales,
  onEditSale,
  onDeleteSale,
}: SalesTableProps) {
  const columns = [
    {
      key: "saleNumber",
      header: "Sale",
    },
    {
      key: "customer",
      header: "Customer",
    },
    {
      key: "saleDate",
      header: "Date",
    },
    {
      key: "amount",
      header: "Amount",
      render: (sale: Sale) =>
        `${sale.currency} ${sale.amount.toLocaleString()}`,
    },
    {
      key: "status",
      header: "Status",
      render: (sale: Sale) => <StatusBadge status={sale.status} />,
    },
    {
      key: "actions",
      header: "Actions",
      render: (sale: Sale) => (
        <div className="flex gap-2">
          <button type="button" onClick={() => onEditSale(sale)}>
            Edit
          </button>
          <button type="button" onClick={() => onDeleteSale(sale)}>
            Delete
          </button>
        </div>
      ),
    },
  ];

  return (
    <Table
      columns={columns}
      data={sales}
      getRowKey={(sale) => sale.id}
      emptyMessage="No sales found."
    />
  );
}
