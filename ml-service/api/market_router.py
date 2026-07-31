from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db

from models.model_type import ModelType

from repositories.stock_repository import StockRepository
from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository
)
from repositories.prediction_repository import (
    PredictionRepository
)
from repositories.model_metrics_repository import (
    ModelMetricsRepository
)

from services.yahoo_service import YahooService
from services.stock_service import StockService
from services.indicator_service import IndicatorService
from services.feature_engineering_service import (
    FeatureEngineeringService
)
from services.training_service import TrainingService
from services.prediction_service import PredictionService
from services.market_pipeline_service import (
    MarketPipelineService
)
from services.market_service import MarketService


router = APIRouter(
    prefix="/market",
    tags=["Market Pipeline"]
)


def get_market_service(db: Session):

    stock_repo = StockRepository(db)
    indicator_repo = TechnicalIndicatorRepository(db)
    prediction_repo = PredictionRepository(db)
    metrics_repo = ModelMetricsRepository(db)

    yahoo_service = YahooService()

    stock_service = StockService(
        stock_repo,
        yahoo_service
    )

    indicator_service = IndicatorService(
        stock_repo,
        indicator_repo
    )

    feature_service = FeatureEngineeringService(
        stock_repo,
        indicator_repo
    )

    training_service = TrainingService(
        feature_service,
        metrics_repo
    )

    prediction_service = PredictionService(
        feature_service,
        prediction_repo,
        metrics_repo
    )

    pipeline = MarketPipelineService(
        stock_service=stock_service,
        indicator_service=indicator_service,
        training_service=training_service,
        prediction_service=prediction_service,
        stock_repository=stock_repo
    )

    return MarketService(
        pipeline
    )


# ---------------------------------------------------------
# Run Complete Pipeline
# ---------------------------------------------------------

@router.post("/run")
def run_pipeline(
    model_type: ModelType = Query(
        default=ModelType.LIGHTGBM
    ),
    tune: bool = Query(
        default=False
    ),
    db: Session = Depends(get_db)
):

    service = get_market_service(db)

    return service.run_pipeline(
        model_type=model_type,
        tune=tune
    )


# ---------------------------------------------------------
# Update Prices
# ---------------------------------------------------------

@router.post("/update")
def update_market(
    db: Session = Depends(get_db)
):

    service = get_market_service(db)

    return service.update_market()


# ---------------------------------------------------------
# Train All Stocks
# ---------------------------------------------------------

@router.post("/train")
def train_market(
    model_type: ModelType = Query(
        default=ModelType.LIGHTGBM
    ),
    tune: bool = Query(
        default=False
    ),
    db: Session = Depends(get_db)
):

    service = get_market_service(db)

    return service.train_market(
        model_type=model_type,
        tune=tune
    )


# ---------------------------------------------------------
# Predict All Stocks
# ---------------------------------------------------------

@router.post("/predict")
def predict_market(
    model_type: ModelType = Query(
        default=ModelType.LIGHTGBM
    ),
    db: Session = Depends(get_db)
):

    service = get_market_service(db)

    return service.predict_market(
        model_type=model_type
    )


# ---------------------------------------------------------
# Status
# ---------------------------------------------------------

@router.get("/status")
def status(
    db: Session = Depends(get_db)
):

    service = get_market_service(db)

    return service.status()