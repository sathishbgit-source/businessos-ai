import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    BillingRecordAccessDenied,
    BillingRecordNotFound,
    BusinessOSError,
    InvitationAlreadyAccepted,
    InvitationAlreadyExists,
    InvitationExpired,
    InvitationNotFound,
    InvitationRevoked,
    InvalidBillingPeriod,
    InvalidSubscriptionPeriod,
    NotificationAccessDenied,
    NotificationNotFound,
    OrganisationAccessDenied,
    OrganisationAlreadyExists,
    OrganisationMemberAlreadyExists,
    OrganisationNotFound,
    PaymentAccessDenied,
    PaymentCustomerMismatch,
    PaymentNotFound,
    PaymentProviderReferenceAlreadyExists,
    PlanAccessDenied,
    PlanInactive,
    PlanNotFound,
    RoleNotFound,
    SubscriptionAccessDenied,
    SubscriptionNotFound,
    SubscriptionStateTransitionDenied,
    UserNotFound,
)

logger = logging.getLogger(__name__)


BUSINESS_EXCEPTION_STATUS_CODES = {
    OrganisationAlreadyExists: status.HTTP_409_CONFLICT,
    OrganisationNotFound: status.HTTP_404_NOT_FOUND,
    OrganisationAccessDenied: status.HTTP_403_FORBIDDEN,
    OrganisationMemberAlreadyExists: status.HTTP_409_CONFLICT,
    UserNotFound: status.HTTP_404_NOT_FOUND,
    RoleNotFound: status.HTTP_404_NOT_FOUND,

    InvitationAlreadyExists: status.HTTP_409_CONFLICT,
    InvitationNotFound: status.HTTP_404_NOT_FOUND,
    InvitationExpired: status.HTTP_410_GONE,
    InvitationRevoked: status.HTTP_410_GONE,
    InvitationAlreadyAccepted: status.HTTP_409_CONFLICT,

    NotificationNotFound: status.HTTP_404_NOT_FOUND,
    NotificationAccessDenied: status.HTTP_403_FORBIDDEN,

    SubscriptionNotFound: status.HTTP_404_NOT_FOUND,
    SubscriptionAccessDenied: status.HTTP_403_FORBIDDEN,
    InvalidSubscriptionPeriod: status.HTTP_400_BAD_REQUEST,
    SubscriptionStateTransitionDenied: status.HTTP_409_CONFLICT,

    BillingRecordNotFound: status.HTTP_404_NOT_FOUND,
    BillingRecordAccessDenied: status.HTTP_403_FORBIDDEN,
    InvalidBillingPeriod: status.HTTP_400_BAD_REQUEST,

    PaymentNotFound: status.HTTP_404_NOT_FOUND,
    PaymentAccessDenied: status.HTTP_403_FORBIDDEN,
    PaymentCustomerMismatch: status.HTTP_400_BAD_REQUEST,
    PaymentProviderReferenceAlreadyExists: status.HTTP_409_CONFLICT,

    PlanNotFound: status.HTTP_404_NOT_FOUND,
    PlanAccessDenied: status.HTTP_403_FORBIDDEN,
    PlanInactive: status.HTTP_409_CONFLICT,
}


BUSINESS_EXCEPTION_CODES = {
    OrganisationAlreadyExists: "ORGANISATION_ALREADY_EXISTS",
    OrganisationNotFound: "ORGANISATION_NOT_FOUND",
    OrganisationAccessDenied: "ORGANISATION_ACCESS_DENIED",
    OrganisationMemberAlreadyExists: "ORGANISATION_MEMBER_ALREADY_EXISTS",
    UserNotFound: "USER_NOT_FOUND",
    RoleNotFound: "ROLE_NOT_FOUND",

    InvitationAlreadyExists: "INVITATION_ALREADY_EXISTS",
    InvitationNotFound: "INVITATION_NOT_FOUND",
    InvitationExpired: "INVITATION_EXPIRED",
    InvitationRevoked: "INVITATION_REVOKED",
    InvitationAlreadyAccepted: "INVITATION_ALREADY_ACCEPTED",

    NotificationNotFound: "NOTIFICATION_NOT_FOUND",
    NotificationAccessDenied: "NOTIFICATION_ACCESS_DENIED",

    SubscriptionNotFound: "SUBSCRIPTION_NOT_FOUND",
    SubscriptionAccessDenied: "SUBSCRIPTION_ACCESS_DENIED",
    InvalidSubscriptionPeriod: "INVALID_SUBSCRIPTION_PERIOD",
    SubscriptionStateTransitionDenied: "SUBSCRIPTION_STATE_TRANSITION_DENIED",

    BillingRecordNotFound: "BILLING_RECORD_NOT_FOUND",
    BillingRecordAccessDenied: "BILLING_RECORD_ACCESS_DENIED",
    InvalidBillingPeriod: "INVALID_BILLING_PERIOD",

    PaymentNotFound: "PAYMENT_NOT_FOUND",
    PaymentAccessDenied: "PAYMENT_ACCESS_DENIED",
    PaymentCustomerMismatch: "PAYMENT_CUSTOMER_MISMATCH",
    PaymentProviderReferenceAlreadyExists: (
        "PAYMENT_PROVIDER_REFERENCE_ALREADY_EXISTS"
    ),

    PlanNotFound: "PLAN_NOT_FOUND",
    PlanAccessDenied: "PLAN_ACCESS_DENIED",
    PlanInactive: "PLAN_INACTIVE",
}


def _business_error_code(exc: BusinessOSError) -> str:
    return BUSINESS_EXCEPTION_CODES.get(
        type(exc),
        "BUSINESS_ERROR",
    )


def _business_error_status(exc: BusinessOSError) -> int:
    return BUSINESS_EXCEPTION_STATUS_CODES.get(
        type(exc),
        status.HTTP_400_BAD_REQUEST,
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register global application exception handlers."""

    @app.exception_handler(BusinessOSError)
    async def business_error_handler(
        request: Request,
        exc: BusinessOSError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=_business_error_status(exc),
            content={
                "success": False,
                "error": {
                    "code": _business_error_code(exc),
                    "message": str(exc),
                    "details": None,
                },
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        detail = exc.detail

        if isinstance(detail, str):
            message = detail
            details = None
        else:
            message = "Request failed"
            details = detail

        return JSONResponse(
            status_code=exc.status_code,
            headers=exc.headers,
            content={
                "success": False,
                "error": {
                    "code": "HTTP_ERROR",
                    "message": message,
                    "details": details,
                },
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        details = []

        for error in exc.errors():
            location = error.get("loc", ())
            field = ".".join(str(item) for item in location)

            details.append(
                {
                    "field": field,
                    "message": error.get(
                        "msg",
                        "Invalid value",
                    ),
                }
            )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": details,
                },
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception(
            "Unhandled application exception",
            exc_info=exc,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "details": None,
                },
            },
        )
