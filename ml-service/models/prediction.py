from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Prediction(BaseModel):
    """
    Response model for stock price prediction.
    """

    symbol: str = Field(
        ...,
        description="Stock symbol"
    )

    current_price: float = Field(
        ...,
        description="Latest market price"
    )

    predicted_price: float = Field(
        ...,
        description="Predicted next closing price"
    )

    change_percent: float = Field(
        ...,
        description="Expected percentage price change"
    )

    signal: str = Field(
        ...,
        description="Trading signal"
    )

    model: str = Field(
        ...,
        description="Machine learning model used"
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=100,
        description="Prediction confidence (%)"
    )

    risk: str = Field(
        ...,
        description="Risk level"
    )

    reasons: List[str] = Field(
        default_factory=list,
        description="Reasons behind the prediction"
    )

    prediction_time: datetime = Field(
        default_factory=datetime.utcnow,
        description="Prediction timestamp"
    )

    class Config:
        from_attributes = True