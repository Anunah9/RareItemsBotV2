"""Модуль для получения цен наклеек, брелков"""

from typing import Protocol


class IItemPriceFetcher(Protocol):
    def get_price_by_name(self, item_name: str) -> dict:
        pass


class MockItemPriceFetcher(IItemPriceFetcher):
    def get_price_by_name(self, item_name):
        return 0
