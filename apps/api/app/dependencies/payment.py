from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.billing_repository import BillingRepository
from app.repositories.organisation_member_repository import (
    OrganisationMemberRepository,
)
from app.repositories.payment_repository import PaymentRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.payment.create_payment import CreatePaymentService
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
