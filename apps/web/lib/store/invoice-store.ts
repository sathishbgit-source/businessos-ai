import { create } from "zustand";
import {
  invoiceData,
  type Invoice,
} from "@/components/invoices/data/invoice-data";

export interface InvoiceInput {
  invoiceNumber: string;
  customer: string;
  issueDate: string;
  dueDate: string;
  amount: number;
  status: Invoice["status"];
  currency: string;
}

export interface InvoiceState {
  invoices: Invoice[];
  isLoading: boolean;
  error: string | null;

  setInvoices: (invoices: Invoice[]) => void;
  addInvoice: (invoice: InvoiceInput) => void;
  updateInvoice: (id: string, updates: Partial<InvoiceInput>) => void;
  deleteInvoice: (id: string) => void;
  clearError: () => void;
}

function getNextInvoiceId(invoices: Invoice[]) {
  const ids = invoices
    .map((invoice) => Number(invoice.id.replace("INV-", "")))
    .filter(Number.isFinite);

  const nextId = Math.max(0, ...ids) + 1;

  return `INV-${String(nextId).padStart(3, "0")}`;
}

export const useInvoiceStore = create<InvoiceState>((set) => ({
  invoices: invoiceData,
  isLoading: false,
  error: null,

  setInvoices: (invoices) => {
    set({
      invoices,
      error: null,
    });
  },

  addInvoice: (invoice) => {
    set((state) => ({
      invoices: [
        ...state.invoices,
        {
          ...invoice,
          id: getNextInvoiceId(state.invoices),
        },
      ],
      error: null,
    }));
  },

  updateInvoice: (id, updates) => {
    set((state) => {
      const invoiceExists = state.invoices.some(
        (invoice) => invoice.id === id,
      );

      if (!invoiceExists) {
        return {
          error: `Invoice ${id} was not found.`,
        };
      }

      return {
        invoices: state.invoices.map((invoice) =>
          invoice.id === id ? { ...invoice, ...updates } : invoice,
        ),
        error: null,
      };
    });
  },

  deleteInvoice: (id) => {
    set((state) => {
      const invoiceExists = state.invoices.some(
        (invoice) => invoice.id === id,
      );

      if (!invoiceExists) {
        return {
          error: `Invoice ${id} was not found.`,
        };
      }

      return {
        invoices: state.invoices.filter((invoice) => invoice.id !== id),
        error: null,
      };
    });
  },

  clearError: () => {
    set({ error: null });
  },
}));
