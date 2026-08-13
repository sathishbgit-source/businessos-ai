import { Input } from "@/components/ui";
import type { InventoryStatus } from "./data/inventory-data";

interface InventoryHeaderProps {
  search: string;
  statusFilter: InventoryStatus | "all";
  locationFilter: string;
  locations: string[];
  onSearchChange: (value: string) => void;
  onStatusFilterChange: (
    value: InventoryStatus | "all",
  ) => void;
  onLocationFilterChange: (value: string) => void;
}

export function InventoryHeader({
  search,
  statusFilter,
  locationFilter,
  locations,
  onSearchChange,
  onStatusFilterChange,
  onLocationFilterChange,
}: InventoryHeaderProps) {
  return (
    <section>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Inventory</h1>
          <p className="text-sm text-muted-foreground">
            Monitor stock levels, reorder points, and inventory locations.
          </p>
        </div>

      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
        <div className="w-full sm:max-w-md">
          <Input
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Search inventory..."
            aria-label="Search inventory"
          />
        </div>

        <label className="flex flex-col gap-1 text-sm">
          <span>Status</span>
          <select
            value={statusFilter}
            onChange={(event) =>
              onStatusFilterChange(
                event.target.value as InventoryStatus | "all",
              )
            }
            className="ui-input"
            aria-label="Filter inventory by status"
          >
            <option value="all">All</option>
            <option value="in_stock">In Stock</option>
            <option value="low_stock">Low Stock</option>
            <option value="out_of_stock">Out of Stock</option>
          </select>
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span>Location</span>
          <select
            value={locationFilter}
            onChange={(event) =>
              onLocationFilterChange(event.target.value)
            }
            className="ui-input"
            aria-label="Filter inventory by location"
          >
            <option value="all">All</option>
            {locations.map((location) => (
              <option key={location} value={location}>
                {location}
              </option>
            ))}
          </select>
        </label>
      </div>
    </section>
  );
}
