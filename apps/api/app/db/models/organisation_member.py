from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base


class OrganisationMember(Base):
    __tablename__ = "organisation_members"

    __table_args__ = (
        UniqueConstraint(
            "organisation_id",
            "user_id",
            name="uq_organisation_member",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    organisation_id: Mapped[UUID] = mapped_column(
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    )
    

    status: Mapped[str] = mapped_column(
        String(20),
        default="ACTIVE",
        nullable=False,
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    organisation: Mapped["Organisation"] = relationship(
        "Organisation",
        back_populates="members",
    )

    user: Mapped["User"] = relationship(
    "User",
    back_populates="organisation_members",
    )
    

    role: Mapped["Role"] = relationship(
        "Role",
    )

    def __repr__(self) -> str:
        return (
            f"OrganisationMember("
            f"organisation_id={self.organisation_id}, "
            f"user_id={self.user_id}, "
            f"role_id={self.role_id})"
        )