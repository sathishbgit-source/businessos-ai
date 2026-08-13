export type InventoryStatus =
  | "in_stock"
  | "low_stock"
  | "out_of_stock";

export interface InventoryItem {
  id: string;
  sku: string;
  productName: string;
  brand: string;
  category: string;
  quantity: number;
  reorderLevel: number;
  location: string;
  status: InventoryStatus;
}

export const inventoryData: InventoryItem[] = [
  {
    id: "INV-001",
    sku: "TYR-205-55-R16",
    productName: "205/55 R16 Passenger Tyre",
    brand: "GRENLANDER",
    category: "PCR",
    quantity: 120,
    reorderLevel: 40,
    location: "Melbourne",
    status: "in_stock",
  },
  {
    id: "INV-002",
    sku: "TYR-215-60-R17",
    productName: "215/60 R17 SUV Tyre",
    brand: "RAPID",
    category: "SUV",
    quantity: 85,
    reorderLevel: 30,
    location: "Melbourne",
    status: "in_stock",
  },
  {
    id: "INV-003",
    sku: "TYR-265-65-R17",
    productName: "265/65 R17 All Terrain Tyre",
    brand: "Landspider",
    category: "AT",
    quantity: 42,
    reorderLevel: 50,
    location: "Brisbane",
    status: "low_stock",
  },
  {
    id: "INV-004",
    sku: "TYR-295-80-R22",
    productName: "295/80 R22.5 Truck Tyre",
    brand: "Powertrac",
    category: "TBR",
    quantity: 24,
    reorderLevel: 20,
    location: "Brisbane",
    status: "in_stock",
  },
  {
    id: "INV-005",
    sku: "TYR-225-75-R16",
    productName: "225/75 R16 Commercial Tyre",
    brand: "Techshield",
    category: "Commercial",
    quantity: 0,
    reorderLevel: 25,
    location: "Melbourne",
    status: "out_of_stock",
  },
];
