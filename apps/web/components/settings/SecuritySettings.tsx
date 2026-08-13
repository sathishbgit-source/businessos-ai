"use client";

import { Select } from "@/components/ui";
import type { SecuritySettings as SecuritySettingsType } from "@/components/settings/data/settings-data";

interface SecuritySettingsProps {
  settings: SecuritySettingsType;
  onChange: (updates: Partial<SecuritySettingsType>) => void;
}

export function SecuritySettings({
  settings,
  onChange,
}: SecuritySettingsProps) {
  return (
    <section className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold">Security</h2>
        <p className="text-sm text-muted-foreground">
          Configure basic session and login preferences.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Select
          id="session-timeout"
          label="Session Timeout"
          value={settings.sessionTimeout}
          options={[
            { value: "15", label: "15 minutes" },
            { value: "30", label: "30 minutes" },
            { value: "60", label: "60 minutes" },
            { value: "120", label: "120 minutes" },
          ]}
          onChange={(event) =>
            onChange({
              sessionTimeout:
                event.target.value as SecuritySettingsType["sessionTimeout"],
            })
          }
        />

        <label className="ui-field">
          <span className="ui-label">Login Alerts</span>
          <span className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={settings.loginAlerts}
              onChange={(event) =>
                onChange({ loginAlerts: event.target.checked })
              }
            />
            <span className="text-sm">
              Alert me when a new login occurs
            </span>
          </span>
        </label>
      </div>
    </section>
  );
}
