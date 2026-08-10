import { Button, Input } from "@/components/ui";
import type { ProductStatus } from "./data/product-data";

interface ProductHeaderProps {
  search: string;
  statusFilter: ProductStatus | "all";
  onSearchChange: (value: string) => void;
  onStatusFilterChange: (value: ProductStatus | "all") => void;
  onAddProduct: () => void;
}

export function ProductHeader({
  search,
  statusFilter,
  onSearchChange,
  onStatusFilterChange,
  onAddProduct,
}: ProductHeaderProps) {
  return (
    <section>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Products</h1>
          <p className="text-sm text-muted-foreground">
            Manage your products, inventory, and pricing.
          </p>
        </div>

        <Button onClick={onAddProduct}>Add Product</Button>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
        <div className="w-full sm:max-w-md">
          <Input
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Search products..."
            aria-label="Search products"
          />
        </div>

        <label className="flex flex-col gap-1 text-sm">
          <span>Status</span>
          <select
            value={statusFilter}
            onChange={(event) =>
              onStatusFilterChange(
                event.target.value as ProductStatus | "all",
              )
            }
            className="ui-input"
            aria-label="Filter products by status"
          >
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="disabled">Disabled</option>
          </select>
        </label>
      </div>
    </section>
  );
}
