import { create } from "zustand";
import {
  subscriptionData,
  type Subscription,
} from "@/components/subscriptions/data/subscription-data";

export interface SubscriptionInput {
  customerId: string;
  planId: string;
  status: Subscription["status"];
  startDate: string;
  currentPeriodStart: string;
  currentPeriodEnd: string;
  createdAt: string;
}

export interface SubscriptionState {
  subscriptions: Subscription[];
  isLoading: boolean;
  error: string | null;

  setSubscriptions: (subscriptions: Subscription[]) => void;
  addSubscription: (subscription: SubscriptionInput) => void;
  updateSubscription: (
    id: string,
    updates: Partial<SubscriptionInput>,
  ) => void;
  deleteSubscription: (id: string) => void;
  clearError: () => void;
}

function getNextSubscriptionId(subscriptions: Subscription[]) {
  const ids = subscriptions
    .map((subscription) =>
      Number(subscription.id.replace("SUB-", "")),
    )
    .filter(Number.isFinite);

  const nextId = Math.max(0, ...ids) + 1;

  return `SUB-${String(nextId).padStart(3, "0")}`;
}

export const useSubscriptionStore = create<SubscriptionState>(
  (set) => ({
    subscriptions: subscriptionData,
    isLoading: false,
    error: null,

    setSubscriptions: (subscriptions) => {
      set({
        subscriptions,
        error: null,
      });
    },

    addSubscription: (subscription) => {
      set((state) => ({
        subscriptions: [
          ...state.subscriptions,
          {
            ...subscription,
            id: getNextSubscriptionId(state.subscriptions),
          },
        ],
        error: null,
      }));
    },

    updateSubscription: (id, updates) => {
      set((state) => {
        const subscriptionExists = state.subscriptions.some(
          (subscription) => subscription.id === id,
        );

        if (!subscriptionExists) {
          return {
            error: `Subscription ${id} was not found.`,
          };
        }

        return {
          subscriptions: state.subscriptions.map(
            (subscription) =>
              subscription.id === id
                ? { ...subscription, ...updates }
                : subscription,
          ),
          error: null,
        };
      });
    },

    deleteSubscription: (id) => {
      set((state) => {
        const subscriptionExists = state.subscriptions.some(
          (subscription) => subscription.id === id,
        );

        if (!subscriptionExists) {
          return {
            error: `Subscription ${id} was not found.`,
          };
        }

        return {
          subscriptions: state.subscriptions.filter(
            (subscription) => subscription.id !== id,
          ),
          error: null,
        };
      });
    },

    clearError: () => {
      set({
        error: null,
      });
    },
  }),
);
