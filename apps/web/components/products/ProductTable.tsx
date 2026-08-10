import { Button, StatusBadge, Table } from "@/components/ui";
import type { Product } from "./data/product-data";

interface ProductTableProps {
  products: Product[];
  onEditProduct: (product: Product) => void;
  onDeleteProduct: (product: Product) => void;
}

export function ProductTable({
  products,
  onEditProduct,
  onDeleteProduct,
}: ProductTableProps) {
  const columns = [
    {
      key: "name",
      header: "Product",
      render: (product: Product) => (
        <div>
          <p className="font-medium">{product.name}</p>
          <p className="text-sm text-muted-foreground">{product.sku}</p>
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
      key: "unitPrice",
      header: "Unit Price",
      render: (product: Product) => `$${product.unitPrice.toFixed(2)}`,
    },
    {
      key: "stockQuantity",
      header: "Stock",
    },
    {
      key: "status",
      header: "Status",
      render: (product: Product) => (
        <StatusBadge status={product.status} />
      ),
    },
    {
      key: "actions",
      header: "Actions",
      render: (product: Product) => (
        <div className="flex gap-2">
          <Button
            variant="ghost"
            onClick={() => onEditProduct(product)}
          >
            Edit
          </Button>
          <Button
            variant="danger"
            onClick={() => onDeleteProduct(product)}
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
      data={products}
      getRowKey={(product) => product.id}
      emptyMessage="No products found."
    />
  );
}
