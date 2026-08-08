from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    __table_args__ = (
        Index("ix_audit_logs_organisation_id", "organisation_id"),
        Index("ix_audit_logs_user_id", "user_id"),
        Index("ix_audit_logs_action", "action"),
        Index("ix_audit_logs_resource", "resource_type", "resource_id"),
        Index("ix_audit_logs_created_at", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    organisation_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "organisations.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    resource_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    resource_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
    )

    event_metadata: Mapped[dict | None] = mapped_column(
        "metadata",
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"AuditLog("
            f"id={self.id}, "
            f"action='{self.action}', "
            f"resource_type='{self.resource_type}', "
            f"resource_id={self.resource_id})"
        )
