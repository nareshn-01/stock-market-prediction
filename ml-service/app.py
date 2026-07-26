from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from database import SessionLocal, engine
from logger import logger
from repositories.stock_repository import StockRepository

# Routes
from routes.download import router as download_router
from routes.indicator import router as indicator_router

# API Routers
from api.prediction_router import router as prediction_router
from api.training_router import router as training_router
from api.metrics_router import router as metrics_router
from api.comparison_router import router as comparison_router
# Scheduler
from scheduler.scheduler import scheduler

app = FastAPI(
    title="Stock ML Service",
    version="1.0.0",
    description="Machine Learning Service for Stock Market Prediction"
)

# ---------------------------------------------------------
# Register Routers
# ---------------------------------------------------------

app.include_router(download_router)
app.include_router(indicator_router)

app.include_router(training_router)
app.include_router(prediction_router)
app.include_router(metrics_router)
app.include_router(comparison_router)
# ---------------------------------------------------------
# Scheduler Events
# ---------------------------------------------------------

@app.on_event("startup")
def startup_event():
    scheduler.start()
    logger.info("Scheduler started successfully.")


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    logger.info("Scheduler stopped.")


# ---------------------------------------------------------
# Home
# ---------------------------------------------------------

@app.get("/")
def home():

    logger.info("Home endpoint accessed")

    return {
        "message": "Stock ML Service Running"
    }


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health():

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    logger.info("Health check successful")

    return {
        "status": "UP",
        "database": "Connected"
    }


# ---------------------------------------------------------
# Get Stock Details
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

            logger.warning(
                f"Stock '{symbol.upper()}' not found"
            )

            raise HTTPException(
                status_code=404,
                detail=f"Stock '{symbol.upper()}' not found"
            )

        logger.info(
            f"Retrieved stock: {stock.symbol}"
        )

        return {
            "id": stock.id,
            "symbol": stock.symbol,
            "company_name": stock.company_name,
            "exchange": stock.exchange,
            "sector": stock.sector,
            "isin": stock.isin
        }

    except Exception as e:

        logger.exception(
            f"Error retrieving stock {symbol}: {e}"
        )

        raise

    finally:

        db.close()