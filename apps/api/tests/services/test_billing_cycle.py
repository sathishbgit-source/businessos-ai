from datetime import datetime, timezone

import pytest

from app.db.enums import BillingInterval
from app.services.billing.billing_cycle import BillingCycleService


def test_calculate_next_monthly_period():
    start = datetime(2026, 1, 15, tzinfo=timezone.utc)
    end = datetime(2026, 2, 15, tzinfo=timezone.utc)

    result = BillingCycleService.calculate_next_period(
        current_period_start=start,
        current_period_end=end,
        billing_interval=BillingInterval.MONTHLY,
    )

    assert result.start == datetime(
        2026, 2, 15, tzinfo=timezone.utc
    )
    assert result.end == datetime(
        2026, 3, 15, tzinfo=timezone.utc
    )


def test_calculate_next_yearly_period():
    start = datetime(2026, 1, 15, tzinfo=timezone.utc)
    end = datetime(2027, 1, 15, tzinfo=timezone.utc)

    result = BillingCycleService.calculate_next_period(
        current_period_start=start,
        current_period_end=end,
        billing_interval=BillingInterval.YEARLY,
    )

    assert result.start == datetime(
        2027, 1, 15, tzinfo=timezone.utc
    )
    assert result.end == datetime(
        2028, 1, 15, tzinfo=timezone.utc
    )


def test_monthly_period_clamps_to_shorter_month():
    start = datetime(2026, 1, 31, tzinfo=timezone.utc)
    end = datetime(2026, 2, 28, tzinfo=timezone.utc)

    result = BillingCycleService.calculate_next_period(
        current_period_start=start,
        current_period_end=end,
        billing_interval=BillingInterval.MONTHLY,
    )

    assert result.start == datetime(
        2026, 2, 28, tzinfo=timezone.utc
    )
    assert result.end == datetime(
        2026, 3, 28, tzinfo=timezone.utc
    )


def test_yearly_period_handles_leap_day():
    start = datetime(2024, 2, 29, tzinfo=timezone.utc)
    end = datetime(2025, 2, 28, tzinfo=timezone.utc)

    result = BillingCycleService.calculate_next_period(
        current_period_start=start,
        current_period_end=end,
        billing_interval=BillingInterval.YEARLY,
    )

    assert result.start == datetime(
        2025, 2, 28, tzinfo=timezone.utc
    )
    assert result.end == datetime(
        2026, 2, 28, tzinfo=timezone.utc
    )


def test_invalid_current_period_is_rejected():
    start = datetime(2026, 2, 15, tzinfo=timezone.utc)
    end = datetime(2026, 2, 15, tzinfo=timezone.utc)

    with pytest.raises(
        ValueError,
        match="Current billing period end must be after start",
    ):
        BillingCycleService.calculate_next_period(
            current_period_start=start,
            current_period_end=end,
            billing_interval=BillingInterval.MONTHLY,
        )


def test_end_before_start_is_rejected():
    start = datetime(2026, 3, 15, tzinfo=timezone.utc)
    end = datetime(2026, 2, 15, tzinfo=timezone.utc)

    with pytest.raises(
        ValueError,
        match="Current billing period end must be after start",
    ):
        BillingCycleService.calculate_next_period(
            current_period_start=start,
            current_period_end=end,
            billing_interval=BillingInterval.YEARLY,
        )
