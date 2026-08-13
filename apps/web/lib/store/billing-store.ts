import { create } from "zustand";
import {
  billingData,
  type BillingRecord,
} from "@/components/billing/data/billing-data";

export interface BillingInput {
  subscriptionId: string;
  customerId: string;
  planId: string;
  billingPeriodStart: string;
  billingPeriodEnd: string;
  amount: number;
  currency: string;
  status: BillingRecord["status"];
}

export interface BillingState {
  billingRecords: BillingRecord[];
  isLoading: boolean;
  error: string | null;

  setBillingRecords: (records: BillingRecord[]) => void;
  addBillingRecord: (record: BillingInput) => void;
  updateBillingRecord: (
    id: string,
    updates: Partial<BillingInput>,
  ) => void;
  deleteBillingRecord: (id: string) => void;
  clearError: () => void;
}

function getNextBillingId(records: BillingRecord[]) {
  const ids = records
    .map((record) =>
      Number(record.id.replace("BIL-", "")),
    )
    .filter(Number.isFinite);

  const nextId = Math.max(0, ...ids) + 1;

  return `BIL-${String(nextId).padStart(3, "0")}`;
}

export const useBillingStore = create<BillingState>((set) => ({
  billingRecords: billingData,
  isLoading: false,
  error: null,

  setBillingRecords: (records) => {
    set({
      billingRecords: records,
      error: null,
    });
  },

  addBillingRecord: (record) => {
    set((state) => ({
      billingRecords: [
        ...state.billingRecords,
        {
          ...record,
          id: getNextBillingId(state.billingRecords),
        },
      ],
      error: null,
    }));
  },

  updateBillingRecord: (id, updates) => {
    set((state) => {
      const recordExists = state.billingRecords.some(
        (record) => record.id === id,
      );

      if (!recordExists) {
        return {
          error: `Billing record ${id} was not found.`,
        };
      }

      return {
        billingRecords: state.billingRecords.map((record) =>
          record.id === id
            ? { ...record, ...updates }
            : record,
        ),
        error: null,
      };
    });
  },

  deleteBillingRecord: (id) => {
    set((state) => {
      const recordExists = state.billingRecords.some(
        (record) => record.id === id,
      );

      if (!recordExists) {
        return {
          error: `Billing record ${id} was not found.`,
        };
      }

      return {
        billingRecords: state.billingRecords.filter(
          (record) => record.id !== id,
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
}));
