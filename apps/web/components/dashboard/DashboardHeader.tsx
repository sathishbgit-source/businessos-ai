interface DashboardHeaderProps {
  title: string;
  description: string;
}

export function DashboardHeader({
  title,
  description,
}: DashboardHeaderProps) {
  return (
    <header className="dashboard-header">
      <div>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>
    </header>
  );
}
