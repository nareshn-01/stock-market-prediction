from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from models import Base


class PriceHistory(Base):
    __tablename__ = "price_history"

    __table_args__ = (
        UniqueConstraint(
            "stock_id",
            "timestamp",
            name="uk_stock_timestamp"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    stock_id: Mapped[int] = mapped_column(
        ForeignKey("stocks.id"),
        nullable=False
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    open: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    high: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    low: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    close: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    volume: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    interval: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    stock: Mapped["Stock"] = relationship(
        lazy="joined"
    )