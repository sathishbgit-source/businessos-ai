export interface Customer {
  id: string;
  name: string;
  company: string;
  email: string;
  phone: string;
  status: "active" | "disabled";
}

export const customerData: Customer[] = [
  {
    id: "CUS-001",
    name: "John Smith",
    company: "Smith Automotive",
    email: "john@smithautomotive.com",
    phone: "+61 400 123 456",
    status: "active",
  },
  {
    id: "CUS-002",
    name: "Michael Brown",
    company: "Brown Motors",
    email: "michael@brownmotors.com",
    phone: "+61 401 234 567",
    status: "active",
  },
  {
    id: "CUS-003",
    name: "David Wilson",
    company: "Wilson Fleet Services",
    email: "david@wilsonfleet.com",
    phone: "+61 402 345 678",
    status: "disabled",
  },
  {
    id: "CUS-004",
    name: "James Taylor",
    company: "Taylor Auto Group",
    email: "james@taylorauto.com",
    phone: "+61 403 456 789",
    status: "active",
  },
  {
    id: "CUS-005",
    name: "Robert Anderson",
    company: "Anderson Logistics",
    email: "robert@andersonlogistics.com",
    phone: "+61 404 567 890",
    status: "active",
  },
  {
    id: "CUS-006",
    name: "Daniel Thomas",
    company: "Thomas Tyres",
    email: "daniel@thomastyres.com",
    phone: "+61 405 678 901",
    status: "disabled",
  },
  {
    id: "CUS-007",
    name: "Chris Martin",
    company: "Martin Automotive",
    email: "chris@martinautomotive.com",
    phone: "+61 406 789 012",
    status: "active",
  },
  {
    id: "CUS-008",
    name: "Andrew Davis",
    company: "Davis Commercial",
    email: "andrew@daviscommercial.com",
    phone: "+61 407 890 123",
    status: "active",
  },
];
