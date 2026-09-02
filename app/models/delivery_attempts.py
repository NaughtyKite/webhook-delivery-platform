import uuid

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base


class DeliveryAttempt(Base):
    __tablename__ = "delivery_attempts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    event_id = Column(
        UUID(as_uuid=True),
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False
    )

    attempt_number = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    response_status_code = Column(
        Integer,
        nullable=True
    )

    error_message = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )