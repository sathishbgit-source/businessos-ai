import calendar
from dataclasses import dataclass
from datetime import datetime

from app.db.enums import BillingInterval


@dataclass(frozen=True)
class BillingPeriod:
    """A calculated billing period."""

    start: datetime
    end: datetime


class BillingCycleService:
    """Calculate subscription billing periods."""

    @staticmethod
    def calculate_next_period(
        *,
        current_period_start: datetime,
        current_period_end: datetime,
        billing_interval: BillingInterval,
    ) -> BillingPeriod:
        """Calculate the next billing period."""

        if current_period_end <= current_period_start:
            raise ValueError(
                "Current billing period end must be after start."
            )

        next_start = current_period_end

        if billing_interval == BillingInterval.MONTHLY:
            next_end = BillingCycleService._add_month(
                next_start
            )
        elif billing_interval == BillingInterval.YEARLY:
            next_end = BillingCycleService._add_year(
                next_start
            )
        else:
            raise ValueError(
                f"Unsupported billing interval: {billing_interval}"
            )

        return BillingPeriod(
            start=next_start,
            end=next_end,
        )

    @staticmethod
    def _add_month(value: datetime) -> datetime:
        """Add one calendar month while clamping the day."""

        if value.month == 12:
            year = value.year + 1
            month = 1
        else:
            year = value.year
            month = value.month + 1

        day = min(
            value.day,
            calendar.monthrange(year, month)[1],
        )

        return value.replace(
            year=year,
            month=month,
            day=day,
        )

    @staticmethod
    def _add_year(value: datetime) -> datetime:
        """Add one calendar year while handling leap day."""

        day = value.day

        if value.month == 2 and value.day == 29:
            day = 28

        return value.replace(
            year=value.year + 1,
            day=day,
        )
