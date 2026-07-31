from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from logger import logger
from models.model_type import ModelType
from services.market_service import MarketService


class SchedulerService:
    """
    Scheduler for automated market operations.
    """

    def __init__(
        self,
        market_service: MarketService
    ):
        self.market_service = market_service
        self.scheduler = BackgroundScheduler()

    # ---------------------------------------------------------
    # Start Scheduler
    # ---------------------------------------------------------

    def start(self):

        logger.info("Starting Market Scheduler...")

        # Daily Market Update
        self.scheduler.add_job(
            func=self.market_service.update_market,
            trigger=CronTrigger(
                day_of_week="mon-fri",
                hour=18,
                minute=0
            ),
            id="daily_market_update",
            replace_existing=True
        )

        # Daily Training
        self.scheduler.add_job(
            func=lambda: self.market_service.train_market(
                model_type=ModelType.LIGHTGBM,
                tune=False
            ),
            trigger=CronTrigger(
                day_of_week="mon-fri",
                hour=18,
                minute=30
            ),
            id="daily_training",
            replace_existing=True
        )

        # Daily Prediction
        self.scheduler.add_job(
            func=lambda: self.market_service.predict_market(
                model_type=ModelType.LIGHTGBM
            ),
            trigger=CronTrigger(
                day_of_week="mon-fri",
                hour=19,
                minute=0
            ),
            id="daily_prediction",
            replace_existing=True
        )

        self.scheduler.start()

        logger.info("Market Scheduler Started.")

    # ---------------------------------------------------------
    # Stop Scheduler
    # ---------------------------------------------------------

    def stop(self):

        self.scheduler.shutdown()

        logger.info("Market Scheduler Stopped.")

    # ---------------------------------------------------------
    # Job Status
    # ---------------------------------------------------------

    def jobs(self):

        return [
            {
                "id": job.id,
                "next_run": str(job.next_run_time)
            }
            for job in self.scheduler.get_jobs()
        ]