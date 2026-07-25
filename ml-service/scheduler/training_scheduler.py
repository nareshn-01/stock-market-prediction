from apscheduler.schedulers.background import BackgroundScheduler

from database import SessionLocal
from repositories.stock_repository import StockRepository
from services.feature_engineering_service import (
    FeatureEngineeringService
)
from services.training_service import TrainingService


class TrainingScheduler:

    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def train_all_models(self):
        """
        Retrain models for all available stocks.
        """
        db = SessionLocal()

        try:
            stock_repository = StockRepository(db)

            feature_service = FeatureEngineeringService()

            training_service = TrainingService(
                feature_service
            )

            stocks = stock_repository.get_all()

            for stock in stocks:
                try:
                    training_service.train(stock)
                    print(
                        f"Model trained successfully for {stock.symbol}"
                    )

                except Exception as ex:
                    print(
                        f"Training failed for {stock.symbol}: {ex}"
                    )

        finally:
            db.close()

    def start(self):
        """
        Start scheduler.
        """

        self.scheduler.add_job(
            self.train_all_models,
            trigger="cron",
            day_of_week="sun",
            hour=18,
            minute=0
        )

        self.scheduler.start()

        print("Training Scheduler Started")