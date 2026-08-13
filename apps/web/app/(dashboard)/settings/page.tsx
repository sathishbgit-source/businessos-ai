"use client";

import { useState } from "react";
import { Button, Toast } from "@/components/ui";
import { SettingsHeader } from "@/components/settings/SettingsHeader";
import { GeneralSettings } from "@/components/settings/GeneralSettings";
import { AppearanceSettings } from "@/components/settings/AppearanceSettings";
import { NotificationSettings } from "@/components/settings/NotificationSettings";
import { SecuritySettings } from "@/components/settings/SecuritySettings";
import { useSettingsStore } from "@/lib/store/settings-store";

export default function SettingsPage() {
  const [saved, setSaved] = useState(false);

  const settings = useSettingsStore((state) => state.settings);
  const updateGeneral = useSettingsStore((state) => state.updateGeneral);
  const updateAppearance = useSettingsStore(
    (state) => state.updateAppearance,
  );
  const updateNotifications = useSettingsStore(
    (state) => state.updateNotifications,
  );
  const updateSecurity = useSettingsStore((state) => state.updateSecurity);
  const resetSettings = useSettingsStore((state) => state.resetSettings);

  const handleSave = () => {
    setSaved(true);
  };

  const handleReset = () => {
    resetSettings();
    setSaved(false);
  };

  return (
    <section className="space-y-6">
      <SettingsHeader />

      {saved ? (
        <Toast
          message="Settings saved successfully."
          variant="success"
          onClose={() => setSaved(false)}
        />
      ) : null}

      <div className="space-y-6">
        <GeneralSettings
          settings={settings.general}
          onChange={updateGeneral}
        />

        <AppearanceSettings
          settings={settings.appearance}
          onChange={updateAppearance}
        />

        <NotificationSettings
          settings={settings.notifications}
          onChange={updateNotifications}
        />

        <SecuritySettings
          settings={settings.security}
          onChange={updateSecurity}
        />
      </div>

      <div className="flex justify-end gap-3">
        <Button type="button" variant="secondary" onClick={handleReset}>
          Reset
        </Button>

        <Button type="button" onClick={handleSave}>
          Save Changes
        </Button>
      </div>
    </section>
  );
}
