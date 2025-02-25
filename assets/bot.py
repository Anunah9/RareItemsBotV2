import asyncio
from asyncio.log import logger
from dataclasses import dataclass
from datetime import datetime
import os
import time
from typing import Protocol
from assets.buy import BuyModule
from assets.config import Config
from assets.parser import Parser, AsyncParser
from assets.session import AsyncSteamSession, SteamSession
from assets.item import AsyncItemData, ItemData
from pprint import pprint
from assets.inspect import IItemInfoFetcher, MockItemInfoFetcher
from assets.prices import IItemPriceFetcher, MockItemPriceFetcher
from assets.utils import create_message, secundomer
from assets.database import Items


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
        config: Config,
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

            item_obj = ItemData(
                self.itemInfoFetcher,
                self.itemPriceFetcher,
                item_name,
                listing_id,
                inspect_link,
                price,
            )
            item_obj.update_item_info()
            message = create_message(item_obj)
            print(message)
            decision = self.calculate_sticker_profitability(item_obj)

    def print_log(item: ItemData):
        print(
            f"Listing {item.listing_id}: Item Price: {item.item_price}, Stickers Price: {item.stickers_price}, Charm Price: {item.charm_price}"
        )

    def calculate_sticker_profitability(self, item: ItemData):
        # Если есть стрик, логику вычисления
        if item.strick.strick:
            profit_threshold = {
                3: self.config.strick3,
                4: self.config.strick45,
                5: self.config.strick45,
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
        config: Config,
        buy_module: BuyModule,
        items: Items,
    ):
        self.session = session
        self.parser = parser
        self.itemInfoFetcher = itemInfoFetcher
        self.itemPriceFetcher = itemPriceFetcher
        self.config: Config = config
        self.buy_module: BuyModule = buy_module
        self.items_manager: Items = items

    async def get_items_from_market(self, item_url):
        raw_data = await self.parser.get_raw_data_from_market(item_url)
        json_data = self.parser.extract_json_from_raw_data(raw_data=raw_data)
        return self.parser.extract_item_data(json_data)

    # TODO Сделать логгирование
    async def create_one_task(self, item_name, item_url: str, delay: float):

        await asyncio.sleep(delay=delay)

        try:
            listings = await self.get_items_from_market(item_url)
        except Exception as exc:
            print(exc)
        else:
            await self.process_items(item_name, listings)

    async def create_task_queue(self, items: list[dict], batch=2, batch_queue=10):
        """
        Создает очередь запросов
        Args:
        items (list[dict]): [{item_name:item_url}, {item_name1:item_url1}] - Список предметов \n
        batch (int) - items/batch -  Количество предметов за одну секунду. \n
        При batch=2 и количестве предметов = 4 в первую секунду создадутся запросы на первые два пердмета, во вторую секунду создадутся следующие два предмета
        """
        # TODO Добавить параметр количество запросов в одном цикле. То есть делать не один цикл а 10 как в старом боте
        tasks = []
        for j in range(batch_queue):
            for i in range(0, len(items)):
                koef = 0.8
                delay = i % batch
                item_name, item_url = next(iter(items[i].items()))
                task = self.create_one_task(
                    item_name, item_url, delay=(j * batch + delay) * koef
                )
                tasks.append(task)
        return tasks

    async def start(self):
        if not self.session.is_alive():
            raise Exception("Session is not alive")
        print("Bot started with an active session.")

        counter = 0
        comleted_requests = 0
        while True:

            print("---------------------------------------")

            items = self.items_manager.get_track_items()
            print(f"Iteration #{counter}")
            pprint(items)
            queue = await self.create_task_queue(items=items, batch=1, batch_queue=20)
            print("Запросов в пачке: ", len(queue))
            comleted_requests += len(queue)
            print("Всего выполненно запросов: ", comleted_requests)
            t1 = time.time()
            await asyncio.gather(*queue)
            print(f"Время выполнения одной пачки: {time.time() - t1}")
            counter += 1

    async def process_items(self, item_name: str, items: list[dict]):

        if not items:
            print(items)
            raise Exception("No items :(")
        for item in items:
            listing_id = item.get("listing_id")
            # TODO Доделать
            if not self.items_manager.check(listing_id):
                self.items_manager.add_to_checked(listing_id)
            else:
                continue
            # TODO
            price = item.get("price")
            fee = item.get("fee")
            if not price:
                print("Item sold")
                continue

            inspect_link = item.get("inspect_link")
            price /= 100
            item_obj = ItemData(
                self.itemInfoFetcher,
                self.itemPriceFetcher,
                item_name,
                listing_id,
                inspect_link,
                price,
            )
            try:
                item_obj.update_item_info()
            except Exception as e:
                print("Запрос к inspect server, завершился с кодом: ", e)
            else:
                message = create_message(item_obj)
                decision = self.calculate_sticker_profitability(item_obj)

                print(message)
                if decision and self.config.autobuy:
                    print("buy")
                    print(message)
                    try:
                        self.buy_module.buy_item(
                            item_name, listing_id, price * 100, fee
                        )

                        self.items_manager.add_to_bought_items(
                            item_name,
                            listing_id,
                            price,
                            item_obj.stickers_price,
                            datetime.now(),
                        )
                        logger.info(
                            f"Bought item {item_name, listing_id, price*100, fee, item_obj.stickers_price}"
                        )
                    except Exception as exc:
                        logger.error(
                            f"Error in buy module:{exc}. Item: {item_name, listing_id, price*100, fee, item_obj.stickers_price}"
                        )
                        print("Ошибка")

    def print_log(item: ItemData):
        print(
            f"Listing {item.listing_id}: Item Price: {item.item_price}, Stickers Price: {item.stickers_price}, Charm Price: {item.charm_price}"
        )

    def calculate_sticker_profitability(self, item: ItemData):
        # Если есть стрик, логику вычисления
        if item.stickers_price < self.config.min_stickers_price:
            return False

        if item.strick.strick:
            profit_threshold = {
                3: self.config.strick3,
                4: self.config.strick45,
                5: self.config.strick45,
            }.get(item.strick.strick_count)

            if profit_threshold:
                sticker_profitability = item.strick.sum_price_strick / item.item_price
                if (
                    sticker_profitability > profit_threshold
                    and item.strick.sum_price_strick > self.config.min_stickers_price
                ):
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
