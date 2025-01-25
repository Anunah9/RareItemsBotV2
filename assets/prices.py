"""Модуль для получения цен наклеек, брелков"""

from typing import Protocol


class IItemPriceFetcher(Protocol):
    def get_price_by_name(self, item_name: str) -> float:
        """Возвращает стоимость предмета по его названию"""
        pass

    def get_stickers_price(stickers: list[dict]) -> float:
        """Возвращает стоимость всех стикеров на скине"""
        pass


class MockItemPriceFetcher(IItemPriceFetcher):
    def get_price_by_name(self, item_name):
        return 0

    def get_stickers_price(self, stickers: list[dict]):
        result_price = 0
        for sticker in stickers:
            result_price += self.get_price_by_name(sticker['name'])
