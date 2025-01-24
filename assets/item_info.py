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
        return {"stickers": [1, 2, 3], "charm": 1433}

    def extract_sticker_info(self, item_info):
        print(item_info["stickers"])

    def extract_charm_info(self, item_info):
        print(item_info["charm"])
