export interface NavigationItem {
  label: string;
  href: string;
}

export const navigationItems: NavigationItem[] = [
  {
    label: "Dashboard",
    href: "/dashboard",
  },
  {
    label: "Customers",
    href: "/customers",
  },
  {
    label: "Products",
    href: "/products",
  },
  {
    label: "Sales",
    href: "/sales",
  },
  {
    label: "Invoices",
    href: "/invoices",
  },
  {
    label: "Payments",
    href: "/payments",
  },
  {
    label: "Notifications",
    href: "/notifications",
  },
  {
    label: "Settings",
    href: "/settings",
  },
];
