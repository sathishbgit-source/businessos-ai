"use client";

import { Select } from "@/components/ui";
import type { AppearanceSettings as AppearanceSettingsType } from "@/components/settings/data/settings-data";

interface AppearanceSettingsProps {
  settings: AppearanceSettingsType;
  onChange: (updates: Partial<AppearanceSettingsType>) => void;
}

export function AppearanceSettings({
  settings,
  onChange,
}: AppearanceSettingsProps) {
  return (
    <section className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold">Appearance</h2>
        <p className="text-sm text-muted-foreground">
          Configure how BusinessOS is displayed.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Select
          id="theme"
          label="Theme"
          value={settings.theme}
          options={[
            { value: "system", label: "System Default" },
            { value: "light", label: "Light" },
            { value: "dark", label: "Dark" },
          ]}
          onChange={(event) =>
            onChange({
              theme: event.target.value as AppearanceSettingsType["theme"],
            })
          }
        />

        <label className="ui-field">
          <span className="ui-label">Compact Mode</span>
          <span className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={settings.compactMode}
              onChange={(event) =>
                onChange({ compactMode: event.target.checked })
              }
            />
            <span className="text-sm">
              Use a more compact interface
            </span>
          </span>
        </label>
      </div>
    </section>
  );
}
