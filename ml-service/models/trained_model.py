from typing import Any

from pydantic import BaseModel, Field


class TrainedModel(BaseModel):
    """
    Response model returned after training a machine learning model.
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
        description="Location of the saved model"
    )

    samples: int = Field(
        ...,
        description="Total samples used for training"
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

    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Model hyperparameters"
    )

    class Config:
        from_attributes = True