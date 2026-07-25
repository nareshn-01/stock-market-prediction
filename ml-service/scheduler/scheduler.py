from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from database import SessionLocal
from logger import logger
from models import stock
from repositories.stock_repository import StockRepository
from services import indicator_service
from services.download_service import DownloadService
from repositories.technical_indicator_repository import TechnicalIndicatorRepository
from services.indicator_service import IndicatorService


def download_all_job():
    logger.info("Starting scheduled stock download...")

    db: Session = SessionLocal()
    total_downloaded = 0
    total_inserted = 0

    try:
        repository = StockRepository(db)
        download_service = DownloadService(repository)

        stocks = repository.get_all_stocks()

        indicator_repo = TechnicalIndicatorRepository(db)

        indicator_svc = IndicatorService(
            repository,
            indicator_repo
        )

        for stock in stocks:
            try:
                result = download_service.download_stock(stock)

                total_downloaded += result.get("records_downloaded", 0)
                total_inserted += result.get("records_inserted", 0)

                logger.info(f"Calculating indicators for {stock.symbol}")

                indicator_result = indicator_svc.calculate_indicators(stock)
                logger.info(f"Indicator result for {stock.symbol}: {indicator_result}")

            except Exception as e:
                db.rollback()
                logger.exception(f"Failed to process {getattr(stock, 'symbol', stock)}: {e}")

        logger.info(f"Download complete. Downloaded={total_downloaded}, Inserted={total_inserted}")

    except Exception:
        logger.exception("Failed to run download_all_job")
    finally:
        db.close()


scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

# Test schedule (runs every minute)
scheduler.add_job(
    download_all_job,
    trigger="interval",
    minutes=1
)
