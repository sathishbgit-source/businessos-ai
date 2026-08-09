"use client";

import { useState } from "react";
import { CustomerHeader } from "@/components/customers/CustomerHeader";
import { CustomerTable } from "@/components/customers/CustomerTable";
import { customerData } from "@/components/customers/data/customer-data";

export default function CustomersPage() {
  const [search, setSearch] = useState("");

  const query = search.trim().toLowerCase();

  const filteredCustomers = query
    ? customerData.filter((customer) =>
        [
          customer.name,
          customer.company,
          customer.email,
          customer.phone,
        ].some((value) => value.toLowerCase().includes(query)),
      )
    : customerData;

  const handleAddCustomer = () => {
    // UI-only action for PR-025.
  };

  return (
    <section className="space-y-6">
      <CustomerHeader
        search={search}
        onSearchChange={setSearch}
        onAddCustomer={handleAddCustomer}
      />

      <CustomerTable customers={filteredCustomers} />
    </section>
  );
}
