from datetime import datetime

from sqlalchemy.orm import Session

from models.technical_indicator import TechnicalIndicator


class TechnicalIndicatorRepository:

    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------------
    # Existing timestamps
    # ---------------------------------------------------------

    def get_existing_timestamps(self, stock_id: int):

        rows = (
            self.db.query(TechnicalIndicator.timestamp)
            .filter(TechnicalIndicator.stock_id == stock_id)
            .all()
        )

        return {row[0] for row in rows}

    # ---------------------------------------------------------
    # Single indicator
    # ---------------------------------------------------------

    def get_by_stock_timestamp(
        self,
        stock_id: int,
        timestamp: datetime,
        interval: str = "1d"
    ):

        return (
            self.db.query(TechnicalIndicator)
            .filter(
                TechnicalIndicator.stock_id == stock_id,
                TechnicalIndicator.timestamp == timestamp,
                TechnicalIndicator.interval == interval
            )
            .first()
        )

    # ---------------------------------------------------------
    # All indicators for a stock
    # ---------------------------------------------------------

    def get_by_stock(
        self,
        stock_id: int,
        interval: str = "1d"
    ):

        return (
            self.db.query(TechnicalIndicator)
            .filter(
                TechnicalIndicator.stock_id == stock_id,
                TechnicalIndicator.interval == interval
            )
            .order_by(TechnicalIndicator.timestamp.asc())
            .all()
        )

    # ---------------------------------------------------------
    # Latest indicator
    # ---------------------------------------------------------

    def get_latest(
        self,
        stock_id: int,
        interval: str = "1d"
    ):

        return (
            self.db.query(TechnicalIndicator)
            .filter(
                TechnicalIndicator.stock_id == stock_id,
                TechnicalIndicator.interval == interval
            )
            .order_by(TechnicalIndicator.timestamp.desc())
            .first()
        )

    # ---------------------------------------------------------
    # Latest N indicators
    # ---------------------------------------------------------

    def get_latest_n(
        self,
        stock_id: int,
        limit: int,
        interval: str = "1d"
    ):

        return (
            self.db.query(TechnicalIndicator)
            .filter(
                TechnicalIndicator.stock_id == stock_id,
                TechnicalIndicator.interval == interval
            )
            .order_by(TechnicalIndicator.timestamp.desc())
            .limit(limit)
            .all()
        )

    # ---------------------------------------------------------
    # Count
    # ---------------------------------------------------------

    def count(
        self,
        stock_id: int,
        interval: str = "1d"
    ):

        return (
            self.db.query(TechnicalIndicator)
            .filter(
                TechnicalIndicator.stock_id == stock_id,
                TechnicalIndicator.interval == interval
            )
            .count()
        )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    def save(self, indicator):

        self.db.add(indicator)

    def save_all(self, indicators):

        self.db.add_all(indicators)

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete(self, indicator):

        self.db.delete(indicator)

    # ---------------------------------------------------------
    # Transaction
    # ---------------------------------------------------------

    def commit(self):

        self.db.commit()

    def rollback(self):

        self.db.rollback()