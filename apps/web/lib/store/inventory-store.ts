import { create } from "zustand";
import {
  inventoryData,
  type InventoryItem,
} from "@/components/inventory/data/inventory-data";

export interface InventoryState {
  inventory: InventoryItem[];
  isLoading: boolean;
  error: string | null;

  setInventory: (inventory: InventoryItem[]) => void;
  updateInventory: (
    id: string,
    updates: Partial<InventoryItem>,
  ) => void;
  adjustStock: (id: string, quantityChange: number) => void;
  clearError: () => void;
}

export const useInventoryStore = create<InventoryState>((set) => ({
  inventory: inventoryData,
  isLoading: false,
  error: null,

  setInventory: (inventory) => {
    set({
      inventory,
      error: null,
    });
  },

  updateInventory: (id, updates) => {
    set((state) => {
      const itemExists = state.inventory.some(
        (item) => item.id === id,
      );

      if (!itemExists) {
        return {
          error: `Inventory item ${id} was not found.`,
        };
      }

      return {
        inventory: state.inventory.map((item) =>
          item.id === id
            ? {
                ...item,
                ...updates,
              }
            : item,
        ),
        error: null,
      };
    });
  },

  adjustStock: (id, quantityChange) => {
    set((state) => {
      const item = state.inventory.find(
        (inventoryItem) => inventoryItem.id === id,
      );

      if (!item) {
        return {
          error: `Inventory item ${id} was not found.`,
        };
      }

      const newQuantity = item.quantity + quantityChange;

      if (newQuantity < 0) {
        return {
          error: `Stock adjustment would make ${item.sku} inventory negative.`,
        };
      }

      const status =
        newQuantity === 0
          ? "out_of_stock"
          : newQuantity <= item.reorderLevel
            ? "low_stock"
            : "in_stock";

      return {
        inventory: state.inventory.map((inventoryItem) =>
          inventoryItem.id === id
            ? {
                ...inventoryItem,
                quantity: newQuantity,
                status,
              }
            : inventoryItem,
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
