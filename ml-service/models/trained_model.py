from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class TrainedModel(BaseModel):
    """
    Metadata for a trained machine learning model.
    """

    symbol: str = Field(
        ...,
        description="Stock symbol"
    )

    algorithm: str = Field(
        ...,
        description="Machine learning algorithm"
    )

    model_path: str = Field(
        ...,
        description="Location of saved model"
    )

    samples: int = Field(
        ...,
        description="Total number of samples used"
    )

    train_samples: int = Field(
        ...,
        description="Training dataset size"
    )

    test_samples: int = Field(
        ...,
        description="Testing dataset size"
    )

    mae: float = Field(
        ...,
        description="Mean Absolute Error"
    )

    rmse: float = Field(
        ...,
        description="Root Mean Squared Error"
    )

    r2: float = Field(
        ...,
        description="R² Score"
    )

    parameters: Optional[dict[str, Any]] = Field(
        default=None,
        description="Best hyperparameters used during training"
    )

    trained_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Training timestamp"
    )

    class Config:
        from_attributes = True