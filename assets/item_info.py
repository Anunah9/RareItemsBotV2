"""Модуль для получения данных о наклейках и брелках"""

from typing import Protocol


class IItemInfoFetcher(Protocol):
    def get_info(self, inspect_link: str) -> dict:
        pass

    def extract_sticker_info(self, item_info: dict) -> None:
        pass

    def extract_charm_info(self, item_info: dict) -> None:
        pass


class MockItemInfoFetcher(IItemInfoFetcher):
    def get_info(self, inspect_link):
        return {
            "stickers": [
                {"name": "Liquid Fire", "wear": 0.5},
                {"name": "Navi", "wear": 0.1},
            ],
            "charm": [{"name": "Loh"}, {"name": "Pidor"}],
        }

    def extract_sticker_info(self, item_info):
        return item_info["stickers"]

    def extract_charm_info(self, item_info):
        return item_info["charm"]
