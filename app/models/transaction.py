from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Transaction(Base):
    """Transaction table."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    transaction_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        default=lambda: str(uuid4()),
    )

    customer_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    merchant_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    merchant_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    merchant_category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="USD",
    )

    payment_method: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    device_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    ip_address: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    risk_score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0,
    )

    fraud_status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
    )

    transaction_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )