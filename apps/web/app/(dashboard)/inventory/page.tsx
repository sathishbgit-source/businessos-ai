"use client";

import { useMemo, useState } from "react";
import { InventoryHeader } from "@/components/inventory/InventoryHeader";
import { InventoryTable } from "@/components/inventory/InventoryTable";
import type {
  InventoryItem,
  InventoryStatus,
} from "@/components/inventory/data/inventory-data";
import { useInventoryStore } from "@/lib/store/inventory-store";

export default function InventoryPage() {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<
    InventoryStatus | "all"
  >("all");
  const [locationFilter, setLocationFilter] = useState("all");

  const inventory = useInventoryStore(
    (state) => state.inventory,
  );
  const error = useInventoryStore((state) => state.error);
  const clearError = useInventoryStore(
    (state) => state.clearError,
  );
  const adjustStock = useInventoryStore(
    (state) => state.adjustStock,
  );

  const locations = useMemo(
    () =>
      Array.from(
        new Set(inventory.map((item) => item.location)),
      ).sort(),
    [inventory],
  );

  const query = search.trim().toLowerCase();

  const filteredInventory = inventory.filter((item) => {
    const matchesSearch =
      !query ||
      [
        item.sku,
        item.productName,
        item.brand,
        item.category,
        item.location,
      ].some((value) =>
        value.toLowerCase().includes(query),
      );

    const matchesStatus =
      statusFilter === "all" ||
      item.status === statusFilter;

    const matchesLocation =
      locationFilter === "all" ||
      item.location === locationFilter;

    return (
      matchesSearch &&
      matchesStatus &&
      matchesLocation
    );
  });

  const handleAdjustStock = (item: InventoryItem) => {
    const value = window.prompt(
      `Adjust stock for ${item.sku}. Enter a positive number to add stock or a negative number to remove stock.`,
      "0",
    );

    if (value === null) {
      return;
    }

    const quantityChange = Number(value);

    if (!Number.isInteger(quantityChange)) {
      return;
    }

    adjustStock(item.id, quantityChange);
  };

  return (
    <section className="space-y-6">
      <InventoryHeader
        search={search}
        statusFilter={statusFilter}
        locationFilter={locationFilter}
        locations={locations}
        onSearchChange={setSearch}
        onStatusFilterChange={setStatusFilter}
        onLocationFilterChange={setLocationFilter}
      />

      {error ? (
        <div role="alert">
          <p>{error}</p>
          <button type="button" onClick={clearError}>
            Dismiss
          </button>
        </div>
      ) : null}

      <InventoryTable
        inventory={filteredInventory}
        onAdjustStock={handleAdjustStock}
      />
    </section>
  );
}
