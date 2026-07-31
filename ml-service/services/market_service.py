from models.model_type import ModelType
from services.market_pipeline_service import (
    MarketPipelineService
)


class MarketService:
    """
    Service responsible for market-wide operations.
    """

    def __init__(
        self,
        pipeline: MarketPipelineService
    ):
        self.pipeline = pipeline

    # ---------------------------------------------------------
    # Complete Pipeline
    # ---------------------------------------------------------

    def run_pipeline(
        self,
        model_type: ModelType = ModelType.LIGHTGBM,
        tune: bool = False
    ):

        return self.pipeline.run(
            model_type=model_type,
            tune=tune
        )

    # ---------------------------------------------------------
    # Update Market
    # ---------------------------------------------------------

    def update_market(self):

        return self.pipeline.update_market()

    # ---------------------------------------------------------
    # Train Market
    # ---------------------------------------------------------

    def train_market(
        self,
        model_type: ModelType = ModelType.LIGHTGBM,
        tune: bool = False
    ):

        return self.pipeline.train_market(
            model_type=model_type,
            tune=tune
        )

    # ---------------------------------------------------------
    # Predict Market
    # ---------------------------------------------------------

    def predict_market(
        self,
        model_type: ModelType = ModelType.LIGHTGBM
    ):

        return self.pipeline.predict_market(
            model_type=model_type
        )

    # ---------------------------------------------------------
    # Market Status
    # ---------------------------------------------------------

    def status(self):

        return {
            "status": "RUNNING",
            "service": "Market Pipeline",
            "version": "v1.0"
        }