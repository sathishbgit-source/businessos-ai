import { Button, StatusBadge, Table } from "@/components/ui";
import type { InventoryItem } from "./data/inventory-data";

interface InventoryTableProps {
  inventory: InventoryItem[];
  onAdjustStock: (item: InventoryItem) => void;
}

export function InventoryTable({
  inventory,
  onAdjustStock,
}: InventoryTableProps) {
  const columns = [
    {
      key: "product",
      header: "Product",
      render: (item: InventoryItem) => (
        <div>
          <p className="font-medium">{item.productName}</p>
          <p className="text-sm text-muted-foreground">{item.sku}</p>
        </div>
      ),
    },
    {
      key: "brand",
      header: "Brand",
    },
    {
      key: "category",
      header: "Category",
    },
    {
      key: "quantity",
      header: "Stock",
    },
    {
      key: "reorderLevel",
      header: "Reorder Level",
    },
    {
      key: "location",
      header: "Location",
    },
    {
      key: "status",
      header: "Status",
      render: (item: InventoryItem) => (
        <StatusBadge
          status={
            item.status === "in_stock"
              ? "active"
              : item.status === "low_stock"
                ? "warning"
                : "disabled"
          }
        />
      ),
    },
    {
      key: "actions",
      header: "Actions",
      render: (item: InventoryItem) => (
        <div className="flex gap-2">
          <Button
            variant="ghost"
            onClick={() => onAdjustStock(item)}
          >
            Adjust
          </Button>
        </div>
      ),
    },
  ];

  return (
    <Table
      columns={columns}
      data={inventory}
      getRowKey={(item) => item.id}
      emptyMessage="No inventory found."
    />
  );
}
