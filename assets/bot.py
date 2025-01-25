from assets.parser import Parser
from assets.session import ISteamSession
from assets.currency_rates import Currency
from pprint import pprint
from assets.item_info import MockItemInfoFetcher
from assets.prices import MockItemPriceFetcher


class SteamBot:
    def __init__(
        self,
        session: ISteamSession,
        parser: Parser,
        itemInfoFetcher: MockItemInfoFetcher,
        itemPriceFetcher: MockItemPriceFetcher,
    ):
        self.session = session
        self.parser = parser
        self.itemInfoFetcher = itemInfoFetcher
        self.itemPriceFetcher = itemPriceFetcher

    def start(self):
        if self.session.is_alive():
            print("Bot started with an active session.")
            item_url = "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20(Field-Tested)"
            items = self.get_items_from_market(item_url)
            self.process_items(items)

    def get_items_from_market(self, item_url):
        raw_data = self.parser.get_raw_data_from_market(item_url)
        json_data = self.parser.exract_json_from_raw_data(raw_data=raw_data)
        return self.parser.extract_item_data(json_data)

    def process_items(self, items):
        for item in items:
            listing_id, price, inspect_link = item
            item_info = self.get_item_info(inspect_link)
            stickers = self.extract_sticker_info(item_info)
            stickers_result_price = self.itemPriceFetcher.get_stickers_price(
                stickers)
            charm = self.extract_charm_info(item_info)
            charm_price = self.itemPriceFetcher.get_price_by_name(
                charm.get("name"))
            self.print_item_prices(stickers)

    def get_item_info(self, inspect_link):
        return self.itemInfoFetcher.get_info(inspect_link=inspect_link)

    def extract_sticker_info(self, item_info):
        return self.itemInfoFetcher.extract_sticker_info(item_info)

    def extract_charm_info(self, item_info):
        return self.itemInfoFetcher.extract_charm_info(item_info)

    def print_item_prices(self, stickers):
        for sticker in stickers:
            sticker_name = sticker["name"]
            sticker_price = self.itemPriceFetcher.get_price_by_name(
                sticker_name)
            print(sticker_name, sticker_price)

            # TODO Получить наклейки и брелки на предмете. Заменить с Mock на нормальную реализацию
            # TODO Получить цены наклеек и брелка. Заменить с Mock на нормальную реализацию
            # TODO Сравнить цену предмета и цену наклеек

        # Основная логика бота
