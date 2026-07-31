from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from database import SessionLocal, engine
from logger import logger

from repositories.stock_repository import StockRepository

# Routers
from routes.download import router as download_router
from routes.indicator import router as indicator_router

from api.training_router import router as training_router
from api.prediction_router import router as prediction_router
from api.metrics_router import router as metrics_router
from api.comparison_router import router as comparison_router
from api.market_router import router as market_router

# Scheduler
from scheduler.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting Stock ML Service...")

    scheduler.start()

    logger.info("Scheduler started.")

    yield

    scheduler.shutdown()

    logger.info("Scheduler stopped.")


app = FastAPI(
    title="Stock ML Service",
    version="1.0.0",
    description="Machine Learning Service for Stock Market Prediction",
    lifespan=lifespan
)

# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------

app.include_router(download_router)
app.include_router(indicator_router)

app.include_router(training_router)
app.include_router(prediction_router)
app.include_router(metrics_router)
app.include_router(comparison_router)
app.include_router(market_router)

# ---------------------------------------------------------
# Home
# ---------------------------------------------------------

@app.get("/")
def home():

    return {

        "message": "Stock ML Service Running",

        "version": "1.0.0"

    }


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get("/health")
def health():

    with engine.connect() as connection:

        connection.execute(
            text("SELECT 1")
        )

    return {

        "status": "UP",

        "database": "Connected"

    }


# ---------------------------------------------------------
# Stock Details
# ---------------------------------------------------------

@app.get("/stocks/{symbol}")
def get_stock(symbol: str):

    db = SessionLocal()

    try:

        repository = StockRepository(db)

        stock = repository.get_stock_by_symbol(
            symbol.upper()
        )

        if stock is None:

            raise HTTPException(
                status_code=404,
                detail=f"{symbol.upper()} not found"
            )

        return {

            "id": stock.id,

            "symbol": stock.symbol,

            "company_name": stock.company_name,

            "exchange": stock.exchange,

            "sector": stock.sector,

            "isin": stock.isin

        }

    finally:

        db.close()