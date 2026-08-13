"use client";

import { Input, Select } from "@/components/ui";
import type { GeneralSettings as GeneralSettingsType } from "@/components/settings/data/settings-data";

interface GeneralSettingsProps {
  settings: GeneralSettingsType;
  onChange: (updates: Partial<GeneralSettingsType>) => void;
}

export function GeneralSettings({
  settings,
  onChange,
}: GeneralSettingsProps) {
  return (
    <section className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold">General</h2>
        <p className="text-sm text-muted-foreground">
          Configure your business and regional defaults.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Input
          id="business-name"
          label="Business Name"
          value={settings.businessName}
          onChange={(event) =>
            onChange({ businessName: event.target.value })
          }
        />

        <Select
          id="currency"
          label="Currency"
          value={settings.currency}
          options={[
            { value: "AUD", label: "AUD — Australian Dollar" },
            { value: "INR", label: "INR — Indian Rupee" },
            { value: "USD", label: "USD — US Dollar" },
          ]}
          onChange={(event) =>
            onChange({
              currency:
                event.target.value as GeneralSettingsType["currency"],
            })
          }
        />

        <Select
          id="timezone"
          label="Timezone"
          value={settings.timezone}
          options={[
            {
              value: "Australia/Melbourne",
              label: "Australia/Melbourne",
            },
            {
              value: "Australia/Brisbane",
              label: "Australia/Brisbane",
            },
            {
              value: "Asia/Kolkata",
              label: "Asia/Kolkata",
            },
            { value: "UTC", label: "UTC" },
          ]}
          onChange={(event) =>
            onChange({
              timezone:
                event.target.value as GeneralSettingsType["timezone"],
            })
          }
        />

        <Select
          id="date-format"
          label="Date Format"
          value={settings.dateFormat}
          options={[
            { value: "DD/MM/YYYY", label: "DD/MM/YYYY" },
            { value: "MM/DD/YYYY", label: "MM/DD/YYYY" },
            { value: "YYYY-MM-DD", label: "YYYY-MM-DD" },
          ]}
          onChange={(event) =>
            onChange({
              dateFormat:
                event.target.value as GeneralSettingsType["dateFormat"],
            })
          }
        />
      </div>
    </section>
  );
}
