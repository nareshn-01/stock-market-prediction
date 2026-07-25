from fastapi import APIRouter, Depends

from database import get_db
from repositories.stock_repository import StockRepository
from services.feature_engineering_service import (
    FeatureEngineeringService
)
from services.training_service import TrainingService

router = APIRouter(
    prefix="/training",
    tags=["Training"]
)


@router.post("/{symbol}")
def train_model(
    symbol: str,
    db=Depends(get_db)
):
    stock_repository = StockRepository(db)

    stock = stock_repository.get_by_symbol(symbol)

    if stock is None:
        raise Exception(
            f"Stock '{symbol}' not found."
        )

    feature_service = FeatureEngineeringService()

    training_service = TrainingService(
        feature_service
    )

    return training_service.train(stock)