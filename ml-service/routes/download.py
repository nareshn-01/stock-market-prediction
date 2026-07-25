from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories.stock_repository import StockRepository
from services.download_service import DownloadService

router = APIRouter(
    prefix="/download",
    tags=["Yahoo Finance"]
)


@router.post("/all")
def download_all_stocks(
    db: Session = Depends(get_db)
):
    repository = StockRepository(db)
    download_service = DownloadService(repository)

    stocks = repository.get_all_stocks()

    total_downloaded = 0
    total_inserted = 0
    failed_stocks = []

    for stock in stocks:
        try:
            result = download_service.download_stock(stock)

            total_downloaded += result["records_downloaded"]
            total_inserted += result["records_inserted"]

        except Exception as e:
            db.rollback()
            failed_stocks.append({
                "symbol": stock.symbol,
                "exchange": stock.exchange,
                "error": str(e)
            })

    return {
        "stocks_processed": len(stocks),
        "records_downloaded": total_downloaded,
        "records_inserted": total_inserted,
        "failed_stocks": failed_stocks
    }


@router.post("/{symbol}")
def download_stock(
    symbol: str,
    db: Session = Depends(get_db)
):
    repository = StockRepository(db)
    download_service = DownloadService(repository)

    stock = repository.get_stock_by_symbol(symbol.upper())

    if stock is None:
        raise HTTPException(
            status_code=404,
            detail="Stock not found"
        )

    try:
        return download_service.download_stock(stock)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )