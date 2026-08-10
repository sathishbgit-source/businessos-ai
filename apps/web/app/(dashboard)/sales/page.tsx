"use client";

import { useState } from "react";
import { SalesHeader } from "@/components/sales/SalesHeader";
import { SalesTable } from "@/components/sales/SalesTable";
import type {
  Sale,
  SaleStatus,
} from "@/components/sales/data/sales-data";
import { useSalesStore } from "@/lib/store/sales-store";

export default function SalesPage() {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<
    SaleStatus | "all"
  >("all");

  const sales = useSalesStore((state) => state.sales);
  const isLoading = useSalesStore((state) => state.isLoading);
  const error = useSalesStore((state) => state.error);
  const addSale = useSalesStore((state) => state.addSale);
  const updateSale = useSalesStore((state) => state.updateSale);
  const deleteSale = useSalesStore((state) => state.deleteSale);
  const clearError = useSalesStore((state) => state.clearError);

  const query = search.trim().toLowerCase();

  const filteredSales = sales.filter((sale) => {
    const matchesSearch =
      !query ||
      [
        sale.saleNumber,
        sale.customer,
        sale.saleDate,
        sale.currency,
      ].some((value) => value.toLowerCase().includes(query));

    const matchesStatus =
      statusFilter === "all" || sale.status === statusFilter;

    return matchesSearch && matchesStatus;
  });

  const handleAddSale = () => {
    addSale({
      saleNumber: "SALE-2026-NEW",
      customer: "New Customer",
      saleDate: "2026-08-10",
      amount: 1000,
      currency: "AUD",
      status: "pending",
    });
  };

  const handleEditSale = (sale: Sale) => {
    updateSale(sale.id, {
      status: sale.status === "pending" ? "completed" : sale.status,
    });
  };

  const handleDeleteSale = (sale: Sale) => {
    deleteSale(sale.id);
  };

  return (
    <section className="space-y-6">
      <SalesHeader
        search={search}
        statusFilter={statusFilter}
        onSearchChange={setSearch}
        onStatusFilterChange={setStatusFilter}
        onAddSale={handleAddSale}
      />

      {error ? (
        <div role="alert">
          <p>{error}</p>
          <button type="button" onClick={clearError}>
            Dismiss
          </button>
        </div>
      ) : null}

      {isLoading ? (
        <p>Loading sales...</p>
      ) : (
        <SalesTable
          sales={filteredSales}
          onEditSale={handleEditSale}
          onDeleteSale={handleDeleteSale}
        />
      )}
    </section>
  );
}
