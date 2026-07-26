from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from database import Base


class ModelMetrics(Base):
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String(20), nullable=False)

    model_name = Column(String(100), nullable=False)

    model_version = Column(String(50), nullable=False)

    mae = Column(Float, nullable=False)

    rmse = Column(Float, nullable=False)

    mape = Column(Float, nullable=False)

    r2_score = Column(Float, nullable=False)

    training_samples = Column(Integer, nullable=False)

    trained_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )