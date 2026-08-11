import { create } from "zustand";
import {
  paymentData,
  type Payment,
} from "@/components/payments/data/payment-data";

export interface PaymentInput {
  paymentNumber: string;
  customer: string;
  paymentDate: string;
  amount: number;
  currency: string;
  method: Payment["method"];
  status: Payment["status"];
}

export interface PaymentState {
  payments: Payment[];
  isLoading: boolean;
  error: string | null;

  setPayments: (payments: Payment[]) => void;
  addPayment: (payment: PaymentInput) => void;
  updatePayment: (id: string, updates: Partial<PaymentInput>) => void;
  deletePayment: (id: string) => void;
  clearError: () => void;
}

function getNextPaymentId(payments: Payment[]) {
  const ids = payments
    .map((payment) => Number(payment.id.replace("PAY-", "")))
    .filter(Number.isFinite);

  const nextId = Math.max(0, ...ids) + 1;

  return `PAY-${String(nextId).padStart(3, "0")}`;
}

export const usePaymentStore = create<PaymentState>((set) => ({
  payments: paymentData,
  isLoading: false,
  error: null,

  setPayments: (payments) => {
    set({
      payments,
      error: null,
    });
  },

  addPayment: (payment) => {
    set((state) => ({
      payments: [
        ...state.payments,
        {
          ...payment,
          id: getNextPaymentId(state.payments),
        },
      ],
      error: null,
    }));
  },

  updatePayment: (id, updates) => {
    set((state) => {
      const paymentExists = state.payments.some(
        (payment) => payment.id === id,
      );

      if (!paymentExists) {
        return {
          error: `Payment ${id} was not found.`,
        };
      }

      return {
        payments: state.payments.map((payment) =>
          payment.id === id ? { ...payment, ...updates } : payment,
        ),
        error: null,
      };
    });
  },

  deletePayment: (id) => {
    set((state) => {
      const paymentExists = state.payments.some(
        (payment) => payment.id === id,
      );

      if (!paymentExists) {
        return {
          error: `Payment ${id} was not found.`,
        };
      }

      return {
        payments: state.payments.filter((payment) => payment.id !== id),
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
