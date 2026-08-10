export type ProductStatus = "active" | "disabled";

export interface Product {
  id: string;
  sku: string;
  name: string;
  brand: string;
  category: string;
  unitPrice: number;
  stockQuantity: number;
  status: ProductStatus;
}

export const productData: Product[] = [
  {
    id: "PRD-001",
    sku: "TYR-205-55-R16",
    name: "205/55 R16 Passenger Tyre",
    brand: "GRENLANDER",
    category: "PCR",
    unitPrice: 82,
    stockQuantity: 120,
    status: "active",
  },
  {
    id: "PRD-002",
    sku: "TYR-215-60-R17",
    name: "215/60 R17 SUV Tyre",
    brand: "RAPID",
    category: "SUV",
    unitPrice: 105,
    stockQuantity: 85,
    status: "active",
  },
  {
    id: "PRD-003",
    sku: "TYR-265-65-R17",
    name: "265/65 R17 All Terrain Tyre",
    brand: "Landspider",
    category: "AT",
    unitPrice: 145,
    stockQuantity: 42,
    status: "active",
  },
  {
    id: "PRD-004",
    sku: "TYR-295-80-R22",
    name: "295/80 R22.5 Truck Tyre",
    brand: "Powertrac",
    category: "TBR",
    unitPrice: 285,
    stockQuantity: 24,
    status: "active",
  },
  {
    id: "PRD-005",
    sku: "TYR-225-75-R16",
    name: "225/75 R16 Commercial Tyre",
    brand: "Techshield",
    category: "Commercial",
    unitPrice: 118,
    stockQuantity: 0,
    status: "disabled",
  },
];
