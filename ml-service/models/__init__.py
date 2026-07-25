from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models so SQLAlchemy registers them
from .stock import Stock
from .price_history import PriceHistory
from .technical_indicator import TechnicalIndicator