import { create } from "zustand";
import {
  productData,
  type Product,
} from "@/components/products/data/product-data";

export interface ProductInput {
  sku: string;
  name: string;
  brand: string;
  category: string;
  unitPrice: number;
  stockQuantity: number;
  status: Product["status"];
}

export interface ProductState {
  products: Product[];
  isLoading: boolean;
  error: string | null;

  setProducts: (products: Product[]) => void;
  addProduct: (product: ProductInput) => void;
  updateProduct: (id: string, updates: Partial<ProductInput>) => void;
  deleteProduct: (id: string) => void;
  clearError: () => void;
}

function getNextProductId(products: Product[]) {
  const ids = products
    .map((product) => Number(product.id.replace("PRD-", "")))
    .filter(Number.isFinite);

  const nextId = Math.max(0, ...ids) + 1;

  return `PRD-${String(nextId).padStart(3, "0")}`;
}

export const useProductStore = create<ProductState>((set) => ({
  products: productData,
  isLoading: false,
  error: null,

  setProducts: (products) => {
    set({
      products,
      error: null,
    });
  },

  addProduct: (product) => {
    set((state) => ({
      products: [
        ...state.products,
        {
          ...product,
          id: getNextProductId(state.products),
        },
      ],
      error: null,
    }));
  },

  updateProduct: (id, updates) => {
    set((state) => {
      const productExists = state.products.some(
        (product) => product.id === id,
      );

      if (!productExists) {
        return {
          error: `Product ${id} was not found.`,
        };
      }

      return {
        products: state.products.map((product) =>
          product.id === id ? { ...product, ...updates } : product,
        ),
        error: null,
      };
    });
  },

  deleteProduct: (id) => {
    set((state) => {
      const productExists = state.products.some(
        (product) => product.id === id,
      );

      if (!productExists) {
        return {
          error: `Product ${id} was not found.`,
        };
      }

      return {
        products: state.products.filter((product) => product.id !== id),
        error: null,
      };
    });
  },

  clearError: () => {
    set({ error: null });
  },
}));
