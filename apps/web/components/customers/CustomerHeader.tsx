import { Button, Input } from "@/components/ui";

interface CustomerHeaderProps {
  search: string;
  onSearchChange: (value: string) => void;
  onAddCustomer: () => void;
}

export function CustomerHeader({
  search,
  onSearchChange,
  onAddCustomer,
}: CustomerHeaderProps) {
  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Customers</h1>
          <p className="text-sm text-muted-foreground">
            Manage your customers and their account information.
          </p>
        </div>

        <Button onClick={onAddCustomer}>Add Customer</Button>
      </div>

      <div className="w-full sm:max-w-md">
        <Input
          value={search}
          onChange={(event) => onSearchChange(event.target.value)}
          placeholder="Search customers..."
          aria-label="Search customers"
        />
      </div>
    </div>
  );
}
