from datetime import datetime

from sqlalchemy.orm import Session

from models.stock import Stock
from models.price_history import PriceHistory


class StockRepository:

    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------------
    # Stock methods
    # ---------------------------------------------------------

    def get_stock_by_symbol(self, symbol: str):

        return (
            self.db.query(Stock)
            .filter(Stock.symbol == symbol)
            .first()
        )

    # Alias for compatibility
    def get_by_symbol(self, symbol: str):
        return self.get_stock_by_symbol(symbol)

    def get_all_stocks(self):

        return (
            self.db.query(Stock)
            .order_by(Stock.symbol.asc())
            .all()
        )

    # Alias for compatibility
    def get_all(self):
        return self.get_all_stocks()

    # ---------------------------------------------------------
    # Price History
    # ---------------------------------------------------------

    def get_existing_timestamps(self, stock_id: int):

        rows = (
            self.db.query(PriceHistory.timestamp)
            .filter(PriceHistory.stock_id == stock_id)
            .all()
        )

        return {row[0] for row in rows}

    def price_exists(
        self,
        stock_id: int,
        timestamp: datetime
    ):

        return (
            self.db.query(PriceHistory)
            .filter(
                PriceHistory.stock_id == stock_id,
                PriceHistory.timestamp == timestamp
            )
            .first()
            is not None
        )

    def get_price_history(self, stock_id: int):

        return (
            self.db.query(PriceHistory)
            .filter(PriceHistory.stock_id == stock_id)
            .order_by(PriceHistory.timestamp.asc())
            .all()
        )

    def get_latest_price(self, stock_id: int):

        return (
            self.db.query(PriceHistory)
            .filter(PriceHistory.stock_id == stock_id)
            .order_by(PriceHistory.timestamp.desc())
            .first()
        )

    def get_latest_n_prices(
        self,
        stock_id: int,
        limit: int
    ):

        return (
            self.db.query(PriceHistory)
            .filter(PriceHistory.stock_id == stock_id)
            .order_by(PriceHistory.timestamp.desc())
            .limit(limit)
            .all()
        )

    def count_prices(self, stock_id: int):

        return (
            self.db.query(PriceHistory)
            .filter(PriceHistory.stock_id == stock_id)
            .count()
        )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    def save_price(self, price: PriceHistory):

        self.db.add(price)

    def save_all_prices(self, prices):

        self.db.add_all(prices)

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete_price(self, price: PriceHistory):

        self.db.delete(price)

    # ---------------------------------------------------------
    # Transaction
    # ---------------------------------------------------------

    def commit(self):

        self.db.commit()

    def rollback(self):

        self.db.rollback()