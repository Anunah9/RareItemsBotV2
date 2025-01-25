"""Модуль для получения данных о наклейках и брелках"""

from typing import Protocol


class IItemInfoFetcher(Protocol):
    def get_sticker_and_charm_info(self, inspect_link: str) -> dict:
        """Получает полную информацию о предмете от inspect сервера"""
        pass

    def extract_sticker_info(self, item_info: dict) -> list[dict]:
        """Получает информацию о стикерах на скине"""
        pass

    def extract_charm_info(self, item_info: dict) -> dict:
        """Получает информацию о брелке на скине"""
        pass


class MockItemInfoFetcher(IItemInfoFetcher):
    def get_sticker_and_charm_info(self, inspect_link):
        return {
            "stickers": [
                {"name": "Liquid Fire", "wear": 0.5},
                {"name": "Navi", "wear": 0.1},
            ],
            "charm": {"name": "Loh"},
        }

    def extract_sticker_info(self, item_info):
        return item_info["stickers"]

    def extract_charm_info(self, item_info):
        return item_info["charm"]
