from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.billing import router as billing_router
from app.api.v1.health import router as health_router
from app.api.v1.invitations import router as invitation_router
from app.api.v1.notifications import router as notification_router
from app.api.v1.plans import router as plan_router
from app.api.v1.subscriptions import router as subscription_router
from app.api.v1.organisations import router as organisation_router


router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(auth_router)
router.include_router(organisation_router)
router.include_router(invitation_router)
router.include_router(notification_router)
router.include_router(plan_router)
router.include_router(subscription_router)
router.include_router(billing_router)
