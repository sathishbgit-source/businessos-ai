import { create } from "zustand";
import {
  planData,
  type Plan,
} from "@/components/plans/data/plan-data";

export interface PlanInput {
  name: string;
  description: string;
  price: number;
  currency: string;
  billingInterval: Plan["billingInterval"];
  features: string[];
  status: Plan["status"];
}

export interface PlanState {
  plans: Plan[];
  isLoading: boolean;
  error: string | null;

  setPlans: (plans: Plan[]) => void;
  addPlan: (plan: PlanInput) => void;
  updatePlan: (id: string, updates: Partial<PlanInput>) => void;
  deletePlan: (id: string) => void;
  clearError: () => void;
}

function getNextPlanId(plans: Plan[]) {
  const ids = plans
    .map((plan) => Number(plan.id.replace("PLN-", "")))
    .filter(Number.isFinite);

  const nextId = Math.max(0, ...ids) + 1;

  return `PLN-${String(nextId).padStart(3, "0")}`;
}

export const usePlanStore = create<PlanState>((set) => ({
  plans: planData,
  isLoading: false,
  error: null,

  setPlans: (plans) => {
    set({
      plans,
      error: null,
    });
  },

  addPlan: (plan) => {
    set((state) => ({
      plans: [
        ...state.plans,
        {
          ...plan,
          id: getNextPlanId(state.plans),
        },
      ],
      error: null,
    }));
  },

  updatePlan: (id, updates) => {
    set((state) => {
      const planExists = state.plans.some(
        (plan) => plan.id === id,
      );

      if (!planExists) {
        return {
          error: `Plan ${id} was not found.`,
        };
      }

      return {
        plans: state.plans.map((plan) =>
          plan.id === id
            ? {
                ...plan,
                ...updates,
              }
            : plan,
        ),
        error: null,
      };
    });
  },

  deletePlan: (id) => {
    set((state) => {
      const planExists = state.plans.some(
        (plan) => plan.id === id,
      );

      if (!planExists) {
        return {
          error: `Plan ${id} was not found.`,
        };
      }

      return {
        plans: state.plans.filter((plan) => plan.id !== id),
        error: null,
      };
    });
  },

  clearError: () => {
    set({
      error: null,
    });
  },
}));
