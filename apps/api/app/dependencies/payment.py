from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.billing_repository import BillingRepository
from app.repositories.dunning_repository import DunningRepository
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.providers.payment.mock import MockPaymentProvider
from app.providers.payment.registry import PaymentProviderRegistry
from app.repositories.payment_repository import PaymentRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.dunning.dunning_service import DunningService
from app.services.payment.create_payment import CreatePaymentService
from app.services.payment.handle_payment_webhook import (
    HandlePaymentWebhookService,
)
from app.services.payment.get_payment import GetPaymentService
from app.services.payment.list_payments import ListPaymentsService
from app.services.payment.update_payment import UpdatePaymentService


def get_create_payment_service(
    db: AsyncSession = Depends(get_db),
) -> CreatePaymentService:
    return CreatePaymentService(
        db=db,
        payment_repository=PaymentRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
        billing_repository=BillingRepository(db),
        subscription_repository=SubscriptionRepository(db),
    )


def get_get_payment_service(
    db: AsyncSession = Depends(get_db),
) -> GetPaymentService:
    return GetPaymentService(
        db=db,
        payment_repository=PaymentRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
    )


def get_list_payments_service(
    db: AsyncSession = Depends(get_db),
) -> ListPaymentsService:
    return ListPaymentsService(
        db=db,
        payment_repository=PaymentRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
    )


def get_update_payment_service(
    db: AsyncSession = Depends(get_db),
) -> UpdatePaymentService:
    return UpdatePaymentService(
        db=db,
        payment_repository=PaymentRepository(db),
        organisation_member_repository=OrganisationMemberRepository(db),
    )


def get_payment_provider_registry() -> PaymentProviderRegistry:
    """Return the configured payment provider registry."""

    registry = PaymentProviderRegistry()
    registry.register("mock", MockPaymentProvider)

    return registry


def get_dunning_service(
    db: AsyncSession = Depends(get_db),
    provider_registry: PaymentProviderRegistry = Depends(
        get_payment_provider_registry,
    ),
) -> DunningService:
    return DunningService(
        db=db,
        dunning_repository=DunningRepository(db),
        payment_repository=PaymentRepository(db),
        billing_repository=BillingRepository(db),
        subscription_repository=SubscriptionRepository(db),
        provider_registry=provider_registry,
    )


def get_handle_payment_webhook_service(
    db: AsyncSession = Depends(get_db),
    provider_registry: PaymentProviderRegistry = Depends(
        get_payment_provider_registry,
    ),
) -> HandlePaymentWebhookService:
    return HandlePaymentWebhookService(
        db=db,
        payment_repository=PaymentRepository(db),
        provider_registry=provider_registry,
        dunning_service=get_dunning_service(
            db=db,
            provider_registry=provider_registry,
        ),
    )
