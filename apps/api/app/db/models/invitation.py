from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.enums import InvitationStatus


class Invitation(Base):
    __tablename__ = "invitations"

    __table_args__ = (
        Index("ix_invitation_organisation_id", "organisation_id"),
        Index("ix_invitation_email", "email"),
        Index("ix_invitation_token_hash", "token_hash"),
        Index("ix_invitation_expires_at", "expires_at"),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    organisation_id: Mapped[UUID] = mapped_column(
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
    )

    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
    )

    status: Mapped[InvitationStatus] = mapped_column(
        String(20),
        default=InvitationStatus.PENDING,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    organisation: Mapped["Organisation"] = relationship(
        "Organisation",
        back_populates="invitations",
    )

    created_by_user: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[created_by],
    )

    role: Mapped["Role"] = relationship(
        "Role",
    )

    def __repr__(self) -> str:
        return (
            f"Invitation("
            f"email='{self.email}', "
            f"status='{self.status}')"
        )