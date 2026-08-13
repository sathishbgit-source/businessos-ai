export type Theme = "light" | "dark" | "system";

export type Currency = "AUD" | "INR" | "USD";

export type DateFormat = "DD/MM/YYYY" | "MM/DD/YYYY" | "YYYY-MM-DD";

export type Timezone =
  | "Australia/Melbourne"
  | "Australia/Brisbane"
  | "Asia/Kolkata"
  | "UTC";

export type SessionTimeout = "15" | "30" | "60" | "120";

export interface GeneralSettings {
  businessName: string;
  currency: Currency;
  timezone: Timezone;
  dateFormat: DateFormat;
}

export interface AppearanceSettings {
  theme: Theme;
  compactMode: boolean;
}

export interface NotificationSettings {
  emailNotifications: boolean;
  paymentAlerts: boolean;
  invoiceAlerts: boolean;
  systemAlerts: boolean;
}

export interface SecuritySettings {
  sessionTimeout: SessionTimeout;
  loginAlerts: boolean;
}

export interface Settings {
  general: GeneralSettings;
  appearance: AppearanceSettings;
  notifications: NotificationSettings;
  security: SecuritySettings;
}

export const defaultSettings: Settings = {
  general: {
    businessName: "BusinessOS",
    currency: "AUD",
    timezone: "Australia/Melbourne",
    dateFormat: "DD/MM/YYYY",
  },
  appearance: {
    theme: "system",
    compactMode: false,
  },
  notifications: {
    emailNotifications: true,
    paymentAlerts: true,
    invoiceAlerts: true,
    systemAlerts: true,
  },
  security: {
    sessionTimeout: "60",
    loginAlerts: true,
  },
};
