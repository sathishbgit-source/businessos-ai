import { create } from "zustand";
import {
  defaultSettings,
  type AppearanceSettings,
  type GeneralSettings,
  type NotificationSettings,
  type SecuritySettings,
  type Settings,
} from "@/components/settings/data/settings-data";

export interface SettingsState {
  settings: Settings;

  updateGeneral: (updates: Partial<GeneralSettings>) => void;
  updateAppearance: (updates: Partial<AppearanceSettings>) => void;
  updateNotifications: (updates: Partial<NotificationSettings>) => void;
  updateSecurity: (updates: Partial<SecuritySettings>) => void;
  resetSettings: () => void;
}

export const useSettingsStore = create<SettingsState>((set) => ({
  settings: defaultSettings,

  updateGeneral: (updates) => {
    set((state) => ({
      settings: {
        ...state.settings,
        general: {
          ...state.settings.general,
          ...updates,
        },
      },
    }));
  },

  updateAppearance: (updates) => {
    set((state) => ({
      settings: {
        ...state.settings,
        appearance: {
          ...state.settings.appearance,
          ...updates,
        },
      },
    }));
  },

  updateNotifications: (updates) => {
    set((state) => ({
      settings: {
        ...state.settings,
        notifications: {
          ...state.settings.notifications,
          ...updates,
        },
      },
    }));
  },

  updateSecurity: (updates) => {
    set((state) => ({
      settings: {
        ...state.settings,
        security: {
          ...state.settings.security,
          ...updates,
        },
      },
    }));
  },

  resetSettings: () => {
    set({
      settings: {
        general: { ...defaultSettings.general },
        appearance: { ...defaultSettings.appearance },
        notifications: { ...defaultSettings.notifications },
        security: { ...defaultSettings.security },
      },
    });
  },
}));
