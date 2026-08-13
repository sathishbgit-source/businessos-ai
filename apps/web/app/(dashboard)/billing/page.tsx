"use client";

import { useState } from "react";
import { BillingHeader } from "@/components/billing/BillingHeader";
import { BillingTable } from "@/components/billing/BillingTable";
import type {
  BillingRecord,
  BillingStatus,
} from "@/components/billing/data/billing-data";
import { useBillingStore } from "@/lib/store/billing-store";

export default function BillingPage() {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<
    BillingStatus | "all"
  >("all");

  const billingRecords = useBillingStore(
    (state) => state.billingRecords,
  );
  const isLoading = useBillingStore(
    (state) => state.isLoading,
  );
  const error = useBillingStore((state) => state.error);
  const addBillingRecord = useBillingStore(
    (state) => state.addBillingRecord,
  );
  const updateBillingRecord = useBillingStore(
    (state) => state.updateBillingRecord,
  );
  const deleteBillingRecord = useBillingStore(
    (state) => state.deleteBillingRecord,
  );
  const clearError = useBillingStore(
    (state) => state.clearError,
  );

  const query = search.trim().toLowerCase();

  const filteredBillingRecords = billingRecords.filter(
    (record) => {
      const matchesSearch =
        !query ||
        [
          record.id,
          record.subscriptionId,
          record.customerId,
          record.planId,
          record.billingPeriodStart,
          record.billingPeriodEnd,
          record.currency,
        ].some((value) =>
          value.toLowerCase().includes(query),
        );

      const matchesStatus =
        statusFilter === "all" ||
        record.status === statusFilter;

      return matchesSearch && matchesStatus;
    },
  );

  const handleAddBillingRecord = () => {
    addBillingRecord({
      subscriptionId: "SUB-005",
      customerId: "CUS-005",
      planId: "PLN-001",
      billingPeriodStart: "2026-08-10",
      billingPeriodEnd: "2026-09-09",
      amount: 29,
      currency: "AUD",
      status: "pending",
    });
  };

  const handleEditBillingRecord = (
    record: BillingRecord,
  ) => {
    updateBillingRecord(record.id, {
      status:
        record.status === "pending"
          ? "billed"
          : record.status === "billed"
            ? "paid"
            : record.status,
    });
  };

  const handleDeleteBillingRecord = (
    record: BillingRecord,
  ) => {
    deleteBillingRecord(record.id);
  };

  return (
    <section className="space-y-6">
      <BillingHeader
        search={search}
        statusFilter={statusFilter}
        onSearchChange={setSearch}
        onStatusFilterChange={setStatusFilter}
        onAddBillingRecord={handleAddBillingRecord}
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
        <p>Loading billing records...</p>
      ) : (
        <BillingTable
          billingRecords={filteredBillingRecords}
          onEditBillingRecord={handleEditBillingRecord}
          onDeleteBillingRecord={handleDeleteBillingRecord}
        />
      )}
    </section>
  );
}
