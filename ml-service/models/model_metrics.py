from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String
)

from database import Base


class ModelMetrics(Base):

    __tablename__ = "model_metrics"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    symbol = Column(
        String,
        nullable=False,
        index=True
    )

    model_name = Column(
        String,
        nullable=False,
        index=True
    )

    model_version = Column(
        String,
        nullable=False,
        default="v1.1"
    )

    mae = Column(
        Float,
        nullable=False
    )

    rmse = Column(
        Float,
        nullable=False,
        index=True
    )

    mape = Column(
        Float,
        nullable=False
    )

    r2_score = Column(
        Float,
        nullable=False
    )

    training_samples = Column(
        Integer,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):

        return (
            f"<ModelMetrics("
            f"symbol='{self.symbol}', "
            f"model='{self.model_name}', "
            f"rmse={self.rmse:.4f}, "
            f"r2={self.r2_score:.4f})>"
        )