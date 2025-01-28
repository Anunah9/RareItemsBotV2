import asyncio
from dataclasses import dataclass
from typing import Protocol
from assets.config import Config
from assets.parser import Parser, AsyncParser
from assets.session import AsyncSteamSession, SteamSession
from assets.item import ItemData
from pprint import pprint
from assets.inspect import IItemInfoFetcher, MockItemInfoFetcher
from assets.prices import IItemPriceFetcher, MockItemPriceFetcher
from assets.utils import create_message


class ISteamBot(Protocol):
    def __init__(
        self,
        session: AsyncSteamSession,
        parser: Parser,
        itemInfoFetcher: IItemInfoFetcher,
        itemPriceFetcher: IItemPriceFetcher,
    ):
        pass

    def start(self):
        pass

    def get_items_from_market(self, item_url):
        pass

    def process_items(self, item_name, items):
        pass

    def get_sticker_and_charm_info(self, inspect_link):
        pass

    def extract_sticker_info(self, item_info):
        pass

    def get_sticker_price(self, stickers):
        pass

    def extract_charm_info(self, item_info):
        pass

    def get_charm_price(self, charm_name: str):
        pass

    def print_log(item: ItemData):
        pass

    def get_decision(self, item: ItemData):
        """Функция определения выгодности лота"""
        pass


class SteamBot:
    def __init__(
        self,
        session: SteamSession,
        parser: Parser,
        itemInfoFetcher: MockItemInfoFetcher,
        itemPriceFetcher: IItemPriceFetcher,
        config: Config
    ):
        self.session = session
        self.parser = parser
        self.itemInfoFetcher = itemInfoFetcher
        self.itemPriceFetcher = itemPriceFetcher
        self.config: Config = config

    def get_items_from_market(self, item_url):
        raw_data = self.parser.get_raw_data_from_market(item_url)
        json_data = self.parser.extract_json_from_raw_data(raw_data=raw_data)
        return self.parser.extract_item_data(json_data)

    def start(self):
        if self.session.is_alive():
            print("Bot started with an active session.")
            item_name = "AK-47|Slate (Field-Tested)"
            item_url = "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20(Field-Tested)"
            items = self.get_items_from_market(item_url)
            self.process_items(item_name, items)

    def process_items(self, item_name, items):

        if not items:
            print(items)
            raise Exception("No items :(")
        for item in items:
            listing_id = item.get("listing_id")
            price = item.get("price")
            if not price:
                print("Item sold")
                continue
            inspect_link = item.get("inspect_link")

            item_obj = ItemData(self.itemInfoFetcher, self.itemPriceFetcher,
                                item_name, listing_id, inspect_link, price)
            item_obj.update_item_info()
            message = create_message(item_obj)
            print(message)
            decision = self.calculate_sticker_profitability(item_obj)

    def print_log(item: ItemData):
        print(f"Listing {item.listing_id}: Item Price: {item.item_price}, Stickers Price: {item.stickers_price}, Charm Price: {item.charm_price}")

    def calculate_sticker_profitability(self, item: ItemData):
        # Если есть стрик, логику вычисления
        if item.strick.strick:
            profit_threshold = {
                3: self.config.strick3,
                4: self.config.strick45,
                5: self.config.strick45
            }.get(item.strick.strick_count)

            if profit_threshold:
                sticker_profitability = item.strick.sum_price_strick / item.item_price
                if sticker_profitability > profit_threshold:
                    print("Покупаем")
                    return True
        else:
            # Когда стрика нет, используем базовую цену стикеров
            sticker_profitability = item.stickers_price / item.item_price
            if sticker_profitability > self.config.nostrick:
                print("Покупаем")
                return True

        return False

    def get_decision(self, item: ItemData) -> bool:

        # Пример логики принятия решения по стрикам
        return


class AsyncSteamBot:
    def __init__(
        self,
        session: AsyncSteamSession,
        parser: AsyncParser,
        itemInfoFetcher: IItemInfoFetcher,
        itemPriceFetcher: IItemPriceFetcher,
        config: Config
    ):
        self.session = session
        self.parser = parser
        self.itemInfoFetcher = itemInfoFetcher
        self.itemPriceFetcher = itemPriceFetcher
        self.config: Config = config

    async def get_items_from_market(self, item_url):
        raw_data = await self.parser.get_raw_data_from_market(item_url)
        json_data = self.parser.extract_json_from_raw_data(raw_data=raw_data)
        return self.parser.extract_item_data(json_data)

    async def create_one_task(self, item_name, item_url: str, delay: float):
        await asyncio.sleep(delay=delay)
        listings = await self.get_items_from_market(item_url)
        self.process_items(item_name, listings)

    async def create_task_queue(self, items: list[dict], batch=1):
        """
        Создает очередь запросов
        Args:
        items (list[dict]): [{item_name:item_url}, {item_name1:item_url1}] - Список предметов \n
        batch (int) - 1/batch -  Количество предметов за одну секунду. \n
        При batch=2 и количестве предметов = 4 в первую секунду создадутся запросы на первые два пердмета, во вторую секунду создадутся следующие два предмета"""
        tasks = []
        print("123123123", items)
        for i in range(0, len(items)):
            delay = i//batch
            item_name, item_url = next(iter(items[i].items()))

            task = self.create_one_task(item_name, item_url, delay=delay)
            tasks.append(task)

        return tasks

    async def start(self):
        if not await self.session.is_alive():
            raise Exception("Session is not alive")
        print("Bot started with an active session.")
        items = [
            {"AK-47 | Slate (Field-Tested)": r"https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20(Field-Tested)"},

            {"AK-47 | Slate (Battle-Scarred)": r"https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20%28Battle-Scarred%29"}
        ]
        for i in range(5):
            print("---------------------------------------")
            print(f"Iteration #{i}")
            queue = await self.create_task_queue(items=items)
            await asyncio.gather(*queue)

    def process_items(self, item_name, items):

        if not items:
            print(items)
            raise Exception("No items :(")
        for item in items:
            listing_id = item.get("listing_id")
            price = item.get("price")
            if not price:
                print("Item sold")
                continue
            inspect_link = item.get("inspect_link")

            item_obj = ItemData(self.itemInfoFetcher, self.itemPriceFetcher,
                                item_name, listing_id, inspect_link, price)
            item_obj.update_item_info()
            message = create_message(item_obj)
            print(message)
            decision = self.calculate_sticker_profitability(item_obj)

    def print_log(item: ItemData):
        print(f"Listing {item.listing_id}: Item Price: {item.item_price}, Stickers Price: {item.stickers_price}, Charm Price: {item.charm_price}")

    def calculate_sticker_profitability(self, item: ItemData):
        # Если есть стрик, логику вычисления
        if item.strick.strick:
            profit_threshold = {
                3: self.config.strick3,
                4: self.config.strick45,
                5: self.config.strick45
            }.get(item.strick.strick_count)

            if profit_threshold:
                sticker_profitability = item.strick.sum_price_strick / item.item_price
                if sticker_profitability > profit_threshold:
                    print("Покупаем")
                    return True
        else:
            # Когда стрика нет, используем базовую цену стикеров
            sticker_profitability = item.stickers_price / item.item_price
            if sticker_profitability > self.config.nostrick:
                print("Покупаем")
                return True

        return False

    def get_decision(self, item: ItemData) -> bool:

        # Пример логики принятия решения по стрикам
        return
