from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta


@dataclass(frozen=True)
class DunningPolicy:
    """Business policy controlling failed-payment recovery."""

    retry_intervals: tuple[timedelta, ...] = (
        timedelta(days=1),
        timedelta(days=2),
        timedelta(days=3),
    )
    grace_period: timedelta = timedelta(days=7)

    @property
    def max_retries(self) -> int:
        return len(self.retry_intervals)

    def next_retry_at(
        self,
        *,
        retry_count: int,
        now: datetime,
    ) -> datetime | None:
        if retry_count >= self.max_retries:
            return None

        return now + self.retry_intervals[retry_count]

    def grace_period_ends_at(
        self,
        *,
        now: datetime,
    ) -> datetime:
        return now + self.grace_period
