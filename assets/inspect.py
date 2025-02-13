"""Модуль для получения данных о наклейках и брелках"""

from typing import Protocol

import aiohttp
import requests


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


class ItemInfoFetcher(IItemInfoFetcher):
    def get_sticker_and_charm_info(self, inspect_link: str) -> dict:
        """Получает полную информацию о предмете от inspect сервера"""
        url = 'http://192.168.0.14:80/'
        params = {
            'url': inspect_link
        }
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(
                f"Request ended with statuscode: {response.status_code}")
        response = response.json()
        return response.get('iteminfo')

    def extract_sticker_info(self, item_info: dict) -> list[dict]:
        """Получает информацию о стикерах на скине"""
        return item_info.get('stickers')

    def extract_charm_info(self, item_info: dict) -> dict:
        """Получает информацию о брелке на скине
        UNDER CONSTRACTION. NOT WORING. RETURN ONLY DEFAULT DICT"""

        return {"name": "Loh"}


class AsyncItemInfoFetcher(IItemInfoFetcher):
    async def get_sticker_and_charm_info(self, inspect_link: str) -> dict:
        """Получает полную информацию о предмете от inspect сервера"""
        url = 'http://192.168.0.14:80/'
        params = {
            'url': inspect_link
        }
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, params=params)
        if response.status != 200:
            print(params)
            raise Exception(
                f"Request ended with statuscode: {response.status}")
        response: dict = await response.json()
        return response.get('iteminfo')

    def extract_sticker_info(self, item_info: dict) -> list[dict]:
        """Получает информацию о стикерах на скине"""
        return item_info.get('stickers')

    def extract_charm_info(self, item_info: dict) -> dict:
        """Получает информацию о брелке на скине
        UNDER CONSTRACTION. NOT WORING. RETURN ONLY DEFAULT DICT"""

        return {"name": "Loh"}
