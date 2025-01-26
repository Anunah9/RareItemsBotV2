from dataclasses import dataclass
from typing import Protocol
from assets.parser import Parser
from assets.session import ISteamSession
from assets.item import ItemData
from pprint import pprint
from assets.inspect import IItemInfoFetcher, MockItemInfoFetcher
from assets.prices import IItemPriceFetcher, MockItemPriceFetcher
from assets.utils import create_message


class ISteamBot(Protocol):
    def __init__(
        self,
        session: ISteamSession,
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
        session: ISteamSession,
        parser: Parser,
        itemInfoFetcher: MockItemInfoFetcher,
        itemPriceFetcher: IItemPriceFetcher,
    ):
        self.session = session
        self.parser = parser
        self.itemInfoFetcher = itemInfoFetcher
        self.itemPriceFetcher = itemPriceFetcher

    def get_items_from_market(self, item_url):
        raw_data = self.parser.get_raw_data_from_market(item_url)
        json_data = self.parser.exract_json_from_raw_data(raw_data=raw_data)
        return self.parser.extract_item_data(json_data)

    def start(self):
        if self.session.is_alive():
            print("Bot started with an active session.")
            # Test version with hardcodede item
            item_name = "AK-47|Slate (Field-Tested)"
            item_url = "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20(Field-Tested)"
            items = self.get_items_from_market(item_url)
            self.process_items(item_name, items)

    def process_items(self, item_name, items):
        for item in items:
            listing_id = item.get("listing_id")
            price = item.get("price")
            inspect_link = item.get("inspect_link")
            item_obj = ItemData(item_name, listing_id, inspect_link,
                                price, *self.get_sticker_and_charm_info(inspect_link))

            decision = self.calculate_sticker_profitability(item_obj)
            message = create_message(item)
            print(message)

    def get_sticker_and_charm_info(self, inspect_link):
        item_info = self.itemInfoFetcher.get_sticker_and_charm_info(
            inspect_link=inspect_link)
        stickers = self.extract_sticker_info(item_info)
        for sticker in stickers:
            sticker["price"] = self.itemPriceFetcher.get_price_by_name(
                sticker.get("name"))

        stickers_price = self.get_stickers_sum_price(stickers)
        charm = self.extract_charm_info(item_info)
        charm_price = self.get_charm_price(charm)
        return stickers, stickers_price, charm, charm_price

    def extract_sticker_info(self, item_info):
        return self.itemInfoFetcher.extract_sticker_info(item_info)

    def get_stickers_sum_price(self, stickers: list[dict]):
        result_price = 0
        for sticker in stickers:
            result_price += sticker['price']
        return result_price

    def extract_charm_info(self, item_info):
        return self.itemInfoFetcher.extract_charm_info(item_info)

    def get_charm_price(self, charm):
        return self.itemPriceFetcher.get_price_by_name(charm.get("name"))

    def print_log(item: ItemData):
        print(
            f"Listing {item.listing_id}: Item Price: {item.item_price}, Stickers Price: {item.stickers_price}, Charm Price: {item.charm_price}")

    def calculate_sticker_profitability(self, item: ItemData):
        """Функция определения выгодности лота. Общая стоимость стикеров / стоимость лота"""
        sticker_profitability = item.stickers_price / item.item_price
        return sticker_profitability

    def get_decision(self, item: ItemData) -> bool:
        """Принимает решаение исходя из фактора """
        return False
