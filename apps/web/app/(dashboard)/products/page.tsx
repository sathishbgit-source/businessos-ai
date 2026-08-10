"use client";

import { useState } from "react";
import { ProductHeader } from "@/components/products/ProductHeader";
import { ProductTable } from "@/components/products/ProductTable";
import type {
  Product,
  ProductStatus,
} from "@/components/products/data/product-data";
import { useProductStore } from "@/lib/store/product-store";

export default function ProductsPage() {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<
    ProductStatus | "all"
  >("all");

  const products = useProductStore((state) => state.products);
  const isLoading = useProductStore((state) => state.isLoading);
  const error = useProductStore((state) => state.error);
  const addProduct = useProductStore((state) => state.addProduct);
  const updateProduct = useProductStore((state) => state.updateProduct);
  const deleteProduct = useProductStore((state) => state.deleteProduct);
  const clearError = useProductStore((state) => state.clearError);

  const query = search.trim().toLowerCase();

  const filteredProducts = products.filter((product) => {
    const matchesSearch =
      !query ||
      [
        product.name,
        product.sku,
        product.brand,
        product.category,
      ].some((value) => value.toLowerCase().includes(query));

    const matchesStatus =
      statusFilter === "all" || product.status === statusFilter;

    return matchesSearch && matchesStatus;
  });

  const handleAddProduct = () => {
    addProduct({
      sku: "TYR-NEW",
      name: "New Product",
      brand: "GRENLANDER",
      category: "PCR",
      unitPrice: 100,
      stockQuantity: 0,
      status: "active",
    });
  };

  const handleEditProduct = (product: Product) => {
    updateProduct(product.id, {
      name: `${product.name} - Updated`,
    });
  };

  const handleDeleteProduct = (product: Product) => {
    deleteProduct(product.id);
  };

  return (
    <section className="space-y-6">
      <ProductHeader
        search={search}
        statusFilter={statusFilter}
        onSearchChange={setSearch}
        onStatusFilterChange={setStatusFilter}
        onAddProduct={handleAddProduct}
      />

      {error ? (
        <div role="alert">
          <p>{error}</p>
          <button type="button" onClick={clearError}>
            Dismiss
          </button>
        </div>
      ) : null}

      {isLoading ? (
        <p>Loading products...</p>
      ) : (
        <ProductTable
          products={filteredProducts}
          onEditProduct={handleEditProduct}
          onDeleteProduct={handleDeleteProduct}
        />
      )}
    </section>
  );
}
