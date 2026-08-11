"use client";

import { useState } from "react";
import { PaymentHeader } from "@/components/payments/PaymentHeader";
import { PaymentTable } from "@/components/payments/PaymentTable";
import type {
  Payment,
  PaymentMethod,
  PaymentStatus,
} from "@/components/payments/data/payment-data";
import { usePaymentStore } from "@/lib/store/payment-store";

export default function PaymentsPage() {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<
    PaymentStatus | "all"
  >("all");
  const [methodFilter, setMethodFilter] = useState<
    PaymentMethod | "all"
  >("all");

  const payments = usePaymentStore((state) => state.payments);
  const isLoading = usePaymentStore((state) => state.isLoading);
  const error = usePaymentStore((state) => state.error);
  const addPayment = usePaymentStore((state) => state.addPayment);
  const updatePayment = usePaymentStore((state) => state.updatePayment);
  const deletePayment = usePaymentStore((state) => state.deletePayment);
  const clearError = usePaymentStore((state) => state.clearError);

  const query = search.trim().toLowerCase();

  const filteredPayments = payments.filter((payment) => {
    const matchesSearch =
      !query ||
      [
        payment.paymentNumber,
        payment.customer,
        payment.paymentDate,
        payment.currency,
      ].some((value) => value.toLowerCase().includes(query));

    const matchesStatus =
      statusFilter === "all" || payment.status === statusFilter;

    const matchesMethod =
      methodFilter === "all" || payment.method === methodFilter;

    return matchesSearch && matchesStatus && matchesMethod;
  });

  const handleAddPayment = () => {
    addPayment({
      paymentNumber: "PAY-2026-NEW",
      customer: "New Customer",
      paymentDate: "2026-08-11",
      amount: 1000,
      currency: "AUD",
      method: "card",
      status: "pending",
    });
  };

  const handleEditPayment = (payment: Payment) => {
    updatePayment(payment.id, {
      status: payment.status === "pending" ? "completed" : payment.status,
    });
  };

  const handleDeletePayment = (payment: Payment) => {
    deletePayment(payment.id);
  };

  return (
    <section className="space-y-6">
      <PaymentHeader
        search={search}
        statusFilter={statusFilter}
        methodFilter={methodFilter}
        onSearchChange={setSearch}
        onStatusFilterChange={setStatusFilter}
        onMethodFilterChange={setMethodFilter}
        onAddPayment={handleAddPayment}
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
        <p>Loading payments...</p>
      ) : (
        <PaymentTable
          payments={filteredPayments}
          onEditPayment={handleEditPayment}
          onDeletePayment={handleDeletePayment}
        />
      )}
    </section>
  );
}
