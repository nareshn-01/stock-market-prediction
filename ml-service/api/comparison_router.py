from fastapi import APIRouter, HTTPException

from database import SessionLocal
from repositories.model_metrics_repository import ModelMetricsRepository
from repositories.stock_repository import StockRepository
from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository
)
from services.feature_engineering_service import FeatureEngineeringService
from services.model_comparison_service import ModelComparisonService
from services.training_service import TrainingService

router = APIRouter(
    prefix="/comparison",
    tags=["Model Comparison"]
)


@router.post("/{symbol}")
def compare_models(symbol: str):

    session = SessionLocal()

    try:

        stock_repository = StockRepository(session)
        indicator_repository = TechnicalIndicatorRepository(session)
        metrics_repository = ModelMetricsRepository(session)

        stock = stock_repository.get_by_symbol(symbol)

        if stock is None:
            raise HTTPException(
                status_code=404,
                detail="Stock not found"
            )

        feature_service = FeatureEngineeringService(
            stock_repository,
            indicator_repository
        )

        training_service = TrainingService(
            feature_service,
            metrics_repository
        )

        comparison_service = ModelComparisonService(
            training_service
        )

        return comparison_service.compare(stock)

    finally:
        session.close()