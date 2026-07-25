from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from repositories.stock_repository import StockRepository
from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository
)
from repositories.prediction_repository import (
    PredictionRepository
)

from services.feature_engineering_service import (
    FeatureEngineeringService
)
from services.training_service import TrainingService
from services.prediction_service import PredictionService
from services.prediction_history_service import (
    PredictionHistoryService
)


router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)


# ---------------------------------------------------------
# Train Single Model
# ---------------------------------------------------------

@router.post("/train/{symbol}")
def train_model(
    symbol: str,
    db: Session = Depends(get_db)
):

    stock_repo = StockRepository(db)
    indicator_repo = TechnicalIndicatorRepository(db)

    stock = stock_repo.get_by_symbol(symbol)

    if stock is None:
        raise HTTPException(
            status_code=404,
            detail="Stock not found."
        )

    feature_service = FeatureEngineeringService(
        stock_repo,
        indicator_repo
    )

    training_service = TrainingService(
        feature_service
    )

    return training_service.train(stock)


# ---------------------------------------------------------
# Predict
# ---------------------------------------------------------

@router.get("/{symbol}")
def predict(
    symbol: str,
    db: Session = Depends(get_db)
):

    stock_repo = StockRepository(db)
    indicator_repo = TechnicalIndicatorRepository(db)
    prediction_repo = PredictionRepository(db)

    stock = stock_repo.get_by_symbol(symbol)

    if stock is None:
        raise HTTPException(
            status_code=404,
            detail="Stock not found."
        )

    feature_service = FeatureEngineeringService(
        stock_repo,
        indicator_repo
    )

    prediction_service = PredictionService(
        feature_service,
        prediction_repo
    )

    return prediction_service.predict(stock)


# ---------------------------------------------------------
# Train All Models
# ---------------------------------------------------------

@router.post("/train-all")
def train_all(
    db: Session = Depends(get_db)
):

    stock_repo = StockRepository(db)
    indicator_repo = TechnicalIndicatorRepository(db)

    feature_service = FeatureEngineeringService(
        stock_repo,
        indicator_repo
    )

    training_service = TrainingService(
        feature_service
    )

    stocks = stock_repo.get_all()

    results = []

    for stock in stocks:
        try:
            results.append(
                training_service.train(stock)
            )
        except Exception as e:
            results.append({
                "symbol": stock.symbol,
                "error": str(e)
            })

    return results


# ---------------------------------------------------------
# Prediction History
# ---------------------------------------------------------

@router.get("/history/{symbol}")
def get_prediction_history(
    symbol: str,
    limit: int = 100,
    db: Session = Depends(get_db)
):

    prediction_repo = PredictionRepository(db)

    history_service = PredictionHistoryService(
        prediction_repo
    )

    history = history_service.get_history(
        symbol,
        limit
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail=f"No prediction history found for {symbol.upper()}."
        )

    return history


# ---------------------------------------------------------
# Latest Prediction
# ---------------------------------------------------------

@router.get("/latest/{symbol}")
def get_latest_prediction(
    symbol: str,
    db: Session = Depends(get_db)
):

    prediction_repo = PredictionRepository(db)

    history_service = PredictionHistoryService(
        prediction_repo
    )

    latest = history_service.get_latest(symbol)

    if latest is None:
        raise HTTPException(
            status_code=404,
            detail=f"No prediction found for {symbol.upper()}."
        )

    return latest


# ---------------------------------------------------------
# Delete Prediction History
# ---------------------------------------------------------

@router.delete("/history/{symbol}")
def delete_prediction_history(
    symbol: str,
    db: Session = Depends(get_db)
):

    prediction_repo = PredictionRepository(db)

    history_service = PredictionHistoryService(
        prediction_repo
    )

    result = history_service.delete_history(symbol)

    if result["deleted_records"] == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No prediction history found for {symbol.upper()}."
        )

    return result