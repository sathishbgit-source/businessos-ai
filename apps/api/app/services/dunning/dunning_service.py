from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.enums import BillingStatus
from app.db.enums import DunningStatus
from app.db.enums import PaymentStatus
from app.db.enums import SubscriptionStatus
from app.db.models.dunning import DunningRecord
from app.db.models.payment import Payment
from app.providers.payment.registry import PaymentProviderRegistry
from app.repositories.billing_repository import BillingRepository
from app.repositories.dunning_repository import DunningRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.dunning.dunning_policy import DunningPolicy


class DunningService:
    """Manage failed-payment recovery and subscription suspension."""

    def __init__(
        self,
        db: AsyncSession,
        dunning_repository: DunningRepository,
        payment_repository: PaymentRepository,
        billing_repository: BillingRepository,
        subscription_repository: SubscriptionRepository,
        provider_registry: PaymentProviderRegistry,
        policy: DunningPolicy | None = None,
    ) -> None:
        self.db = db
        self.dunning_repository = dunning_repository
        self.payment_repository = payment_repository
        self.billing_repository = billing_repository
        self.subscription_repository = subscription_repository
        self.provider_registry = provider_registry
        self.policy = policy or DunningPolicy()

    async def start(
        self,
        *,
        payment: Payment,
        now: datetime,
    ) -> DunningRecord:
        """Start dunning for a failed payment."""

        existing = await self.dunning_repository.get_by_billing_record(
            organisation_id=payment.organisation_id,
            billing_record_id=payment.billing_record_id,
        )

        if existing is not None:
            return existing

        next_retry_at = self.policy.next_retry_at(
            retry_count=0,
            now=now,
        )

        dunning = DunningRecord(
            organisation_id=payment.organisation_id,
            subscription_id=payment.subscription_id,
            billing_record_id=payment.billing_record_id,
            status=(
                DunningStatus.RETRYING
                if next_retry_at is not None
                else DunningStatus.GRACE_PERIOD
            ),
            retry_count=0,
            next_retry_at=next_retry_at,
            grace_period_ends_at=None,
        )

        if next_retry_at is None:
            dunning.grace_period_ends_at = (
                self.policy.grace_period_ends_at(now=now)
            )

        await self.dunning_repository.add(dunning)

        billing_record = await self.billing_repository.get_by_id(
            payment.billing_record_id
        )
        if billing_record is not None:
            billing_record.status = BillingStatus.FAILED

        await self.db.flush()

        return dunning

    async def retry(
        self,
        *,
        dunning: DunningRecord,
        now: datetime,
    ) -> Payment | None:
        """Create and submit the next payment attempt when due."""

        if dunning.status != DunningStatus.RETRYING:
            return None

        if (
            dunning.next_retry_at is not None
            and dunning.next_retry_at > now
        ):
            return None

        subscription = await self.subscription_repository.get_by_id(
            dunning.subscription_id
        )

        if subscription is None:
            return None

        if subscription.status != SubscriptionStatus.ACTIVE:
            return None

        billing_record = await self.billing_repository.get_by_id(
            dunning.billing_record_id
        )

        if billing_record is None:
            return None

        provider_name = await self._resolve_provider(
            billing_record_id=dunning.billing_record_id,
        )

        payment = Payment(
            organisation_id=dunning.organisation_id,
            billing_record_id=dunning.billing_record_id,
            subscription_id=dunning.subscription_id,
            customer_id=subscription.customer_id,
            amount=billing_record.amount,
            currency=billing_record.currency.upper(),
            status=PaymentStatus.PENDING,
            provider=provider_name,
        )

        payment = await self.payment_repository.create(payment)

        provider = self.provider_registry.get(provider_name)

        result = await provider.create_payment(
            amount=payment.amount,
            currency=payment.currency,
            payment_id=str(payment.id),
        )

        payment.provider_payment_id = result.provider_payment_id

        dunning.retry_count += 1

        next_retry_at = self.policy.next_retry_at(
            retry_count=dunning.retry_count,
            now=now,
        )

        if next_retry_at is None:
            dunning.status = DunningStatus.GRACE_PERIOD
            dunning.next_retry_at = None
            dunning.grace_period_ends_at = (
                self.policy.grace_period_ends_at(now=now)
            )
        else:
            dunning.next_retry_at = next_retry_at

        await self.db.flush()

        return payment

    async def recover(
        self,
        *,
        payment: Payment,
    ) -> DunningRecord | None:
        """Mark the billing recovery successful."""

        dunning = await self.dunning_repository.get_by_billing_record(
            organisation_id=payment.organisation_id,
            billing_record_id=payment.billing_record_id,
        )

        if dunning is None:
            return None

        dunning.status = DunningStatus.RECOVERED
        dunning.next_retry_at = None
        dunning.grace_period_ends_at = None

        billing_record = await self.billing_repository.get_by_id(
            payment.billing_record_id
        )

        if billing_record is not None:
            billing_record.status = BillingStatus.PAID

        subscription = await self.subscription_repository.get_by_id(
            payment.subscription_id
        )

        if (
            subscription is not None
            and subscription.status == SubscriptionStatus.SUSPENDED
        ):
            subscription.status = SubscriptionStatus.ACTIVE

        await self.db.flush()

        return dunning

    async def suspend(
        self,
        *,
        dunning: DunningRecord,
        now: datetime,
    ) -> DunningRecord:
        """Suspend a subscription after grace-period expiry."""

        if dunning.status != DunningStatus.GRACE_PERIOD:
            return dunning

        if (
            dunning.grace_period_ends_at is not None
            and dunning.grace_period_ends_at > now
        ):
            return dunning

        subscription = await self.subscription_repository.get_by_id(
            dunning.subscription_id
        )

        if subscription is not None:
            subscription.status = SubscriptionStatus.SUSPENDED

        dunning.status = DunningStatus.SUSPENDED
        dunning.next_retry_at = None

        await self.db.flush()

        return dunning

    async def _resolve_provider(
        self,
        *,
        billing_record_id: UUID,
    ) -> str:
        """Resolve the provider from the latest payment attempt."""

        payments = await self.payment_repository.get_all_by_billing_record(
            billing_record_id
        )

        if not payments:
            raise ValueError(
                "Cannot retry a billing record without a payment attempt."
            )

        provider = payments[0].provider.strip().lower()

        if not self.provider_registry.has(provider):
            raise ValueError(
                f"Payment provider '{provider}' is not registered."
            )

        return provider
