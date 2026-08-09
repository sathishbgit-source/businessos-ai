import { Card } from "../ui";
import type { RecentActivity as RecentActivityItem } from "./data/dashboard-data";

interface RecentActivityProps {
  activities: RecentActivityItem[];
}

export function RecentActivity({ activities }: RecentActivityProps) {
  return (
    <Card
      title="Recent Activity"
      description="Latest activity across your business."
    >
      <div className="dashboard-activity-list">
        {activities.map((activity) => (
          <div
            key={activity.title}
            className="dashboard-activity-item"
          >
            <div>
              <strong>{activity.title}</strong>
              <p>{activity.description}</p>
            </div>
            <time>{activity.time}</time>
          </div>
        ))}
      </div>
    </Card>
  );
}
