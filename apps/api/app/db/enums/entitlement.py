from enum import Enum


class Feature(str, Enum):
    BASIC_REPORTS = "basic_reports"
    ADVANCED_REPORTS = "advanced_reports"
    AUTOMATION = "automation"
    ADVANCED_CONTROLS = "advanced_controls"
    CUSTOM_FEATURES = "custom_features"
