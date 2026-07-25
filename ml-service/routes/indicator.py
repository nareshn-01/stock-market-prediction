from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from repositories.stock_repository import StockRepository
from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository
)
from services.indicator_service import IndicatorService

router = APIRouter(
    prefix="/indicators",
    tags=["Indicators"]
)


@router.post("/{symbol}")
def calculate(
    symbol: str,
    db: Session = Depends(get_db)
):

    stock_repo = StockRepository(db)
    indicator_repo = TechnicalIndicatorRepository(db)

    stock = stock_repo.get_stock_by_symbol(symbol.upper())

    if stock is None:
        raise HTTPException(
            status_code=404,
            detail=f"Stock '{symbol.upper()}' not found"
        )

    service = IndicatorService(
        stock_repo,
        indicator_repo
    )

    return service.calculate_indicators(stock)