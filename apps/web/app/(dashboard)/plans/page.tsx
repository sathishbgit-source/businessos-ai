"use client";

import { useState } from "react";
import { PlansHeader } from "@/components/plans/PlansHeader";
import { PlansTable } from "@/components/plans/PlansTable";
import type {
  BillingInterval,
  Plan,
  PlanStatus,
} from "@/components/plans/data/plan-data";
import { usePlanStore } from "@/lib/store/plan-store";

export default function PlansPage() {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<
    PlanStatus | "all"
  >("all");
  const [billingIntervalFilter, setBillingIntervalFilter] =
    useState<BillingInterval | "all">("all");

  const plans = usePlanStore((state) => state.plans);
  const isLoading = usePlanStore((state) => state.isLoading);
  const error = usePlanStore((state) => state.error);
  const addPlan = usePlanStore((state) => state.addPlan);
  const updatePlan = usePlanStore((state) => state.updatePlan);
  const deletePlan = usePlanStore((state) => state.deletePlan);
  const clearError = usePlanStore((state) => state.clearError);

  const query = search.trim().toLowerCase();

  const filteredPlans = plans.filter((plan) => {
    const matchesSearch =
      !query ||
      [
        plan.name,
        plan.description,
        plan.currency,
        plan.billingInterval,
      ].some((value) => value.toLowerCase().includes(query));

    const matchesStatus =
      statusFilter === "all" || plan.status === statusFilter;

    const matchesBillingInterval =
      billingIntervalFilter === "all" ||
      plan.billingInterval === billingIntervalFilter;

    return (
      matchesSearch &&
      matchesStatus &&
      matchesBillingInterval
    );
  });

  const handleAddPlan = () => {
    addPlan({
      name: "New Plan",
      description: "New subscription plan.",
      price: 49,
      currency: "AUD",
      billingInterval: "monthly",
      features: ["Core business management"],
      status: "active",
    });
  };

  const handleEditPlan = (plan: Plan) => {
    updatePlan(plan.id, {
      description: `${plan.description} - Updated`,
    });
  };

  const handleDeletePlan = (plan: Plan) => {
    deletePlan(plan.id);
  };

  return (
    <section className="space-y-6">
      <PlansHeader
        search={search}
        statusFilter={statusFilter}
        billingIntervalFilter={billingIntervalFilter}
        onSearchChange={setSearch}
        onStatusFilterChange={setStatusFilter}
        onBillingIntervalFilterChange={setBillingIntervalFilter}
        onAddPlan={handleAddPlan}
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
        <p>Loading plans...</p>
      ) : (
        <PlansTable
          plans={filteredPlans}
          onEditPlan={handleEditPlan}
          onDeletePlan={handleDeletePlan}
        />
      )}
    </section>
  );
}
