from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from repositories.model_metrics_repository import (
    ModelMetricsRepository
)
from services.model_metrics_service import (
    ModelMetricsService
)

router = APIRouter(
    prefix="/metrics",
    tags=["Model Metrics"]
)


@router.get("/")
def get_all_metrics(
    db=Depends(get_db)
):
    repository = ModelMetricsRepository(db)
    service = ModelMetricsService(repository)

    return service.get_all()


@router.get("/latest/{symbol}")
def get_latest_metrics(
    symbol: str,
    db=Depends(get_db)
):
    repository = ModelMetricsRepository(db)
    service = ModelMetricsService(repository)

    metrics = service.get_latest(symbol.upper())

    if metrics is None:
        raise HTTPException(
            status_code=404,
            detail=f"No metrics found for '{symbol.upper()}'."
        )

    return metrics


@router.get("/{symbol}")
def get_metrics_by_symbol(
    symbol: str,
    db=Depends(get_db)
):
    repository = ModelMetricsRepository(db)
    service = ModelMetricsService(repository)

    metrics = service.get_by_symbol(symbol.upper())

    if not metrics:
        raise HTTPException(
            status_code=404,
            detail=f"No metrics found for '{symbol.upper()}'."
        )

    return metrics


@router.delete("/{symbol}")
def delete_metrics(
    symbol: str,
    db=Depends(get_db)
):
    repository = ModelMetricsRepository(db)
    service = ModelMetricsService(repository)

    deleted = service.delete(symbol.upper())

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No metrics found for '{symbol.upper()}'."
        )

    db.commit()

    return {
        "message": f"Deleted {deleted} metric record(s) for '{symbol.upper()}'."
    }