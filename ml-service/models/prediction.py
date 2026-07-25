from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Prediction(BaseModel):
    """
    Prediction response model.
    """

    symbol: str = Field(
        ...,
        description="Stock symbol"
    )

    current_price: float = Field(
        ...,
        description="Current closing price"
    )

    predicted_price: float = Field(
        ...,
        description="Predicted next closing price"
    )

    change_percent: float = Field(
        ...,
        description="Expected percentage change"
    )

    signal: str = Field(
        ...,
        description="Trading signal"
    )

    prediction_time: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Prediction timestamp"
    )

    class Config:
        from_attributes = True