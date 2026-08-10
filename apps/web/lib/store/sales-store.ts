import { create } from "zustand";
import type { Sale } from "@/components/sales/data/sales-data";
import { salesData } from "@/components/sales/data/sales-data";

interface AddSaleInput {
  saleNumber: string;
  customer: string;
  saleDate: string;
  amount: number;
  currency: string;
  status: Sale["status"];
}

interface UpdateSaleInput {
  saleNumber?: string;
  customer?: string;
  saleDate?: string;
  amount?: number;
  currency?: string;
  status?: Sale["status"];
}

interface SalesState {
  sales: Sale[];
  isLoading: boolean;
  error: string | null;
  addSale: (sale: AddSaleInput) => void;
  updateSale: (id: string, updates: UpdateSaleInput) => void;
  deleteSale: (id: string) => void;
  clearError: () => void;
}

export const useSalesStore = create<SalesState>((set) => ({
  sales: salesData,
  isLoading: false,
  error: null,

  addSale: (sale) =>
    set((state) => ({
      sales: [
        ...state.sales,
        {
          ...sale,
          id: `sale-${Date.now()}`,
        },
      ],
      error: null,
    })),

  updateSale: (id, updates) =>
    set((state) => ({
      sales: state.sales.map((sale) =>
        sale.id === id
          ? {
              ...sale,
              ...updates,
            }
          : sale,
      ),
      error: null,
    })),

  deleteSale: (id) =>
    set((state) => ({
      sales: state.sales.filter((sale) => sale.id !== id),
      error: null,
    })),

  clearError: () =>
    set({
      error: null,
    }),
}));
