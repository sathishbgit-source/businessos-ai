import { Card } from "../ui";

interface QuickActionsProps {
  actions: string[];
}

export function QuickActions({ actions }: QuickActionsProps) {
  return (
    <Card
      title="Quick Actions"
      description="Common actions to manage your business."
    >
      <div className="dashboard-actions">
        {actions.map((action) => (
          <button
            key={action}
            type="button"
            className="dashboard-action"
          >
            {action}
          </button>
        ))}
      </div>
    </Card>
  );
}
