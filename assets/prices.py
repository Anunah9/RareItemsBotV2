"""Модуль для получения цен наклеек, брелков"""

from typing import Protocol


class IItemPriceFetcher(Protocol):
    def __init__(db_repostiotory):
        pass

    def get_price_by_name(self, item_name: str) -> float:
        """Возвращает стоимость предмета по его названию"""
        pass


class MockItemPriceFetcher(IItemPriceFetcher):
    def get_price_by_name(self, item_name):
        return 500
