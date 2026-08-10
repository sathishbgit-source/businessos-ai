"use client";

import { useState } from "react";
import { InvoiceHeader } from "@/components/invoices/InvoiceHeader";
import { InvoiceTable } from "@/components/invoices/InvoiceTable";
import type {
  Invoice,
  InvoiceStatus,
} from "@/components/invoices/data/invoice-data";
import { useInvoiceStore } from "@/lib/store/invoice-store";

export default function InvoicesPage() {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<
    InvoiceStatus | "all"
  >("all");

  const invoices = useInvoiceStore((state) => state.invoices);
  const isLoading = useInvoiceStore((state) => state.isLoading);
  const error = useInvoiceStore((state) => state.error);
  const addInvoice = useInvoiceStore((state) => state.addInvoice);
  const updateInvoice = useInvoiceStore((state) => state.updateInvoice);
  const deleteInvoice = useInvoiceStore((state) => state.deleteInvoice);
  const clearError = useInvoiceStore((state) => state.clearError);

  const query = search.trim().toLowerCase();

  const filteredInvoices = invoices.filter((invoice) => {
    const matchesSearch =
      !query ||
      [
        invoice.invoiceNumber,
        invoice.customer,
        invoice.issueDate,
        invoice.dueDate,
      ].some((value) => value.toLowerCase().includes(query));

    const matchesStatus =
      statusFilter === "all" || invoice.status === statusFilter;

    return matchesSearch && matchesStatus;
  });

  const handleAddInvoice = () => {
    addInvoice({
      invoiceNumber: "INV-2026-NEW",
      customer: "New Customer",
      issueDate: "2026-08-10",
      dueDate: "2026-08-24",
      amount: 1000,
      status: "draft",
      currency: "AUD",
    });
  };

  const handleEditInvoice = (invoice: Invoice) => {
    updateInvoice(invoice.id, {
      status: invoice.status === "draft" ? "sent" : invoice.status,
    });
  };

  const handleDeleteInvoice = (invoice: Invoice) => {
    deleteInvoice(invoice.id);
  };

  return (
    <section className="space-y-6">
      <InvoiceHeader
        search={search}
        statusFilter={statusFilter}
        onSearchChange={setSearch}
        onStatusFilterChange={setStatusFilter}
        onAddInvoice={handleAddInvoice}
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
        <p>Loading invoices...</p>
      ) : (
        <InvoiceTable
          invoices={filteredInvoices}
          onEditInvoice={handleEditInvoice}
          onDeleteInvoice={handleDeleteInvoice}
        />
      )}
    </section>
  );
}
