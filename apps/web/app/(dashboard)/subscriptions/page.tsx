"use client";

import { useState } from "react";
import { SubscriptionHeader } from "@/components/subscriptions/SubscriptionHeader";
import { SubscriptionTable } from "@/components/subscriptions/SubscriptionTable";
import type {
  Subscription,
  SubscriptionStatus,
} from "@/components/subscriptions/data/subscription-data";
import { useSubscriptionStore } from "@/lib/store/subscription-store";

export default function SubscriptionsPage() {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<
    SubscriptionStatus | "all"
  >("all");

  const subscriptions = useSubscriptionStore(
    (state) => state.subscriptions,
  );
  const isLoading = useSubscriptionStore(
    (state) => state.isLoading,
  );
  const error = useSubscriptionStore((state) => state.error);
  const addSubscription = useSubscriptionStore(
    (state) => state.addSubscription,
  );
  const updateSubscription = useSubscriptionStore(
    (state) => state.updateSubscription,
  );
  const deleteSubscription = useSubscriptionStore(
    (state) => state.deleteSubscription,
  );
  const clearError = useSubscriptionStore(
    (state) => state.clearError,
  );

  const query = search.trim().toLowerCase();

  const filteredSubscriptions = subscriptions.filter(
    (subscription) => {
      const matchesSearch =
        !query ||
        [
          subscription.id,
          subscription.customerId,
          subscription.planId,
          subscription.status,
          subscription.startDate,
          subscription.currentPeriodStart,
          subscription.currentPeriodEnd,
        ].some((value) =>
          value.toLowerCase().includes(query),
        );

      const matchesStatus =
        statusFilter === "all" ||
        subscription.status === statusFilter;

      return matchesSearch && matchesStatus;
    },
  );

  const handleAddSubscription = () => {
    addSubscription({
      customerId: "CUS-005",
      planId: "PLN-001",
      status: "active",
      startDate: "2026-08-10",
      currentPeriodStart: "2026-08-10",
      currentPeriodEnd: "2026-09-09",
      createdAt: "2026-08-10",
    });
  };

  const handleEditSubscription = (
    subscription: Subscription,
  ) => {
    updateSubscription(subscription.id, {
      status:
        subscription.status === "active"
          ? "cancelled"
          : "active",
    });
  };

  const handleDeleteSubscription = (
    subscription: Subscription,
  ) => {
    deleteSubscription(subscription.id);
  };

  return (
    <section className="space-y-6">
      <SubscriptionHeader
        search={search}
        statusFilter={statusFilter}
        onSearchChange={setSearch}
        onStatusFilterChange={setStatusFilter}
        onAddSubscription={handleAddSubscription}
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
        <p>Loading subscriptions...</p>
      ) : (
        <SubscriptionTable
          subscriptions={filteredSubscriptions}
          onEditSubscription={handleEditSubscription}
          onDeleteSubscription={handleDeleteSubscription}
        />
      )}
    </section>
  );
}
