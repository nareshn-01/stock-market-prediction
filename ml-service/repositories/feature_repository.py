import pandas as pd

from repositories.stock_repository import StockRepository
from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository
)
from utils.feature_generator import FeatureGenerator


class FeatureRepository:

    def __init__(
        self,
        stock_repository: StockRepository,
        indicator_repository: TechnicalIndicatorRepository
    ):
        self.stock_repository = stock_repository
        self.indicator_repository = indicator_repository

    def get_features(self, symbol: str) -> pd.DataFrame:
        """
        Returns a feature dataframe for the given stock symbol.
        """

        stocks = self.stock_repository.get_by_symbol(symbol)

        indicators = self.indicator_repository.get_by_symbol(symbol)

        if not stocks:
            raise ValueError(
                f"No stock data found for {symbol}"
            )

        if not indicators:
            raise ValueError(
                f"No indicator data found for {symbol}"
            )

        return FeatureGenerator.generate(
            stocks=stocks,
            indicators=indicators
        )

    def exists(self, symbol: str) -> bool:
        """
        Returns True if both stock and indicator data exist.
        """

        return (
            len(self.stock_repository.get_by_symbol(symbol)) > 0
            and
            len(self.indicator_repository.get_by_symbol(symbol)) > 0
        )

    def get_available_symbols(self) -> list[str]:
        """
        Returns all available stock symbols.
        """

        return self.stock_repository.get_symbols()