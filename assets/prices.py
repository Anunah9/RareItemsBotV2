"""Модуль для получения цен наклеек, брелков"""
import os
from pprint import pprint
import sqlite3
from typing import Protocol
import requests
from currency_rates import Currency


class IPricesRepository(Protocol):
    def __init__(self, db_path):
        pass

    def get_price_by_name(self, item_name):
        pass

    def update_all_prices(self):
        pass


class PricesRepository(IPricesRepository):
    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)

    def update_price(self, sticker_name, price):
        query = f'INSERT INTO StickerPrices VALUES ("{sticker_name}", {price})'
        self.db.cursor().execute(query)
        self.db.commit()


class IItemPriceFetcher(Protocol):
    def __init__(db_repostiotory):
        pass

    def get_price_by_name(self, item_name: str) -> float:
        """Возвращает стоимость предмета по его названию"""
        pass

    def update_prices(self, sticker_name, price):
        pass


class MockItemPriceFetcher(IItemPriceFetcher):
    def get_price_by_name(self, item_name):
        return 500


class ItemPriceFetcher:

    def __init__(self, db_repostiotory: PricesRepository, currency: Currency):
        self.repository = db_repostiotory
        self.currency = currency

    def get_price_by_name(self, item_name: str) -> float:
        """Возвращает стоимость предмета по его названию"""
        pass

    def get_all_prices(self):
        url = 'https://www.csbackpack.net/api/items?page=1&max=300000&price_real_min=0&price_real_max=100000&item_group' \
            '=sticker'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers).json()

        return response

    def update_all_prices(self):
        prices = self.get_all_prices()
        for sticker in prices:
            sticker_name = sticker['markethashname']
            # pprint(sticker)
            if sticker['sold30d'] > 10:
                sticker_price = sticker['pricelatest']
                # print(sticker_name, sticker_price)
                converted_price = self.currency.change_currency(
                    sticker_price, 1001)
                self.repository.update_price(
                    sticker_name, round(converted_price, 2))

        print('Цены обновлены.')
        for sticker in prices:
            sticker_name = sticker_name.replace('&#39', "'")

        prices = self.get_all_prices()


if __name__ == "__main__":
    API_KEY = os.getenv("API_KEY")
    currency_rates = Currency(API_KEY)
    currency_rates.update_steam_currency_rates()
    price_repository = PricesRepository("./db.db")
    item_price_fetcher = ItemPriceFetcher(
        db_repostiotory=price_repository, currency=currency_rates)
    item_price_fetcher.update_all_prices()
