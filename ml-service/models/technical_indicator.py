from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    UniqueConstraint,
    Index
)
from sqlalchemy.sql import func

from models import Base


class TechnicalIndicator(Base):
    __tablename__ = "technical_indicators"

    __table_args__ = (
        UniqueConstraint(
            "stock_id",
            "timestamp",
            "interval",
            name="uk_technical_indicator"
        ),
        Index(
            "idx_indicator_stock_timestamp",
            "stock_id",
            "timestamp"
        ),
    )

    id = Column(BigInteger, primary_key=True)

    stock_id = Column(
        BigInteger,
        ForeignKey("stocks.id", ondelete="CASCADE"),
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    interval = Column(
        String(20),
        nullable=False,
        default="1d"
    )

    # ======================
    # Moving Averages
    # ======================

    sma_20 = Column(Numeric(18, 6))
    sma_50 = Column(Numeric(18, 6))
    sma_200 = Column(Numeric(18, 6))

    ema_12 = Column(Numeric(18, 6))
    ema_26 = Column(Numeric(18, 6))

    # ======================
    # Momentum Indicators
    # ======================

    rsi_14 = Column(Numeric(18, 6))

    macd = Column(Numeric(18, 6))
    macd_signal = Column(Numeric(18, 6))
    macd_histogram = Column(Numeric(18, 6))

    # ======================
    # Volatility Indicators
    # ======================

    bb_upper = Column(Numeric(18, 6))
    bb_middle = Column(Numeric(18, 6))
    bb_lower = Column(Numeric(18, 6))

    atr_14 = Column(Numeric(18, 6))

    # ======================
    # Trend Strength Indicators
    # ======================

    plus_di_14 = Column(Numeric(18, 6))
    minus_di_14 = Column(Numeric(18, 6))
    dx_14 = Column(Numeric(18, 6))
    adx_14 = Column(Numeric(18, 6))

    # ======================
    # Audit
    # ======================

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )