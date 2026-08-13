"use client";

import type { NotificationSettings as NotificationSettingsType } from "@/components/settings/data/settings-data";

interface NotificationSettingsProps {
  settings: NotificationSettingsType;
  onChange: (updates: Partial<NotificationSettingsType>) => void;
}

const notificationOptions = [
  {
    key: "emailNotifications",
    label: "Email Notifications",
    description: "Receive important BusinessOS notifications by email.",
  },
  {
    key: "paymentAlerts",
    label: "Payment Alerts",
    description: "Receive alerts when payments are received or fail.",
  },
  {
    key: "invoiceAlerts",
    label: "Invoice Alerts",
    description: "Receive alerts about invoice activity and due dates.",
  },
  {
    key: "systemAlerts",
    label: "System Alerts",
    description: "Receive important application and system alerts.",
  },
] as const;

export function NotificationSettings({
  settings,
  onChange,
}: NotificationSettingsProps) {
  return (
    <section className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold">Notifications</h2>
        <p className="text-sm text-muted-foreground">
          Choose which notifications you want to receive.
        </p>
      </div>

      <div className="space-y-4">
        {notificationOptions.map((option) => (
          <label
            key={option.key}
            className="flex items-start gap-3"
          >
            <input
              type="checkbox"
              checked={settings[option.key]}
              onChange={(event) =>
                onChange({
                  [option.key]: event.target.checked,
                })
              }
            />

            <span>
              <span className="block font-medium">
                {option.label}
              </span>
              <span className="block text-sm text-muted-foreground">
                {option.description}
              </span>
            </span>
          </label>
        ))}
      </div>
    </section>
  );
}
