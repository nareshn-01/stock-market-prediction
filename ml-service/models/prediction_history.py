from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String
)

from database import Base


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    symbol = Column(
        String(20),
        nullable=False,
        index=True
    )

    current_price = Column(
        Float,
        nullable=False
    )

    predicted_price = Column(
        Float,
        nullable=False
    )

    change_percent = Column(
        Float,
        nullable=False
    )

    signal = Column(
        String(20),
        nullable=False
    )

    prediction_time = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )