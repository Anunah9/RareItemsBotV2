from dataclasses import dataclass
from typing import Counter

from assets.inspect import IItemInfoFetcher
from assets.prices import IItemPriceFetcher


class StickerStrick:
    strick: bool
    sticker_name: str
    single_sticker_price: float
    sum_price_strick: float

    def update_strick_counter(self, stickers):
        sticker_names = [sticker.get("name") for sticker in stickers]
        strick_dict = dict(Counter(sticker_names))
        strick = list(filter(lambda x: x[1] >= 3, strick_dict.items()))
        if not strick:
            self.strick = False
        else:
            self.strick = True
            (self.sticker_name, self.strick_count),  = strick

            self.single_sticker_price = list(filter(lambda x: x.get(
                "name") == self.sticker_name, stickers))[0].get("price")
            self.sum_price_strick = self.single_sticker_price*self.strick_count


class ItemData:

    stickers: list[dict]
    stickers_price: float
    charm: dict
    charm_price: float
    strick: StickerStrick

    def __init__(self, itemInfoFetcher: IItemInfoFetcher,
                 itemPriceFetcher: IItemPriceFetcher,
                 item_name: str,
                 listing_id: str,
                 inspect_link: str,
                 item_price: float):
        self.itemInfoFetcher = itemInfoFetcher
        self.itemPriceFetcher = itemPriceFetcher
        self.item_name = item_name
        self.listing_id = listing_id
        self.inspect_link = inspect_link
        self.item_price = item_price

    def update_stickers_prices(self):
        for sticker in self.stickers:
            sticker["price"] = self.itemPriceFetcher.get_price_by_name(
                sticker.get("name"))

    def get_charm_price(self):
        return self.itemPriceFetcher.get_price_by_name(
            self.charm.get("name"))

    def update_item_info(self):
        # All info about item
        item_info = self.itemInfoFetcher.get_sticker_and_charm_info(
            self.inspect_link)

        # Stickers
        self.stickers = self.extract_sticker_info(item_info)

        self.update_stickers_prices()
        self.stickers_price = self.get_stickers_sum_price(self.stickers)

        # Charm
        self.charm = self.extract_charm_info(item_info)
        self.charm_price = self.get_charm_price()

        # Strick
        self.strick = StickerStrick()
        self.strick.update_strick_counter(self.stickers)

    def extract_sticker_info(self, item_info):
        stickers = item_info.get("stickers", [])
        res_stickers = []
        for sticker in stickers:
            if not sticker.get("wear", None):
                res_stickers.append(sticker)
        return res_stickers

    def extract_charm_info(self, item_info):
        return item_info.get("charm", {})

    def get_stickers_sum_price(self, stickers):
        return sum(sticker['price'] for sticker in stickers)


class AsyncItemData:
    stickers: list[dict]
    stickers_price: float
    charm: dict
    charm_price: float
    strick: StickerStrick

    def __init__(self, itemInfoFetcher: IItemInfoFetcher,
                 itemPriceFetcher: IItemPriceFetcher,
                 item_name: str,
                 listing_id: str,
                 inspect_link: str,
                 item_price: float):
        self.itemInfoFetcher = itemInfoFetcher
        self.itemPriceFetcher = itemPriceFetcher
        self.item_name = item_name
        self.listing_id = listing_id
        self.inspect_link = inspect_link
        self.item_price = item_price

    def update_stickers_prices(self):
        for sticker in self.stickers:
            sticker["price"] = self.itemPriceFetcher.get_price_by_name(
                sticker.get("name"))

    def get_charm_price(self):
        return self.itemPriceFetcher.get_price_by_name(
            self.charm.get("name"))

    async def update_item_info(self):
        # All info about item
        item_info = self.itemInfoFetcher.get_sticker_and_charm_info(
            self.inspect_link)

        # Stickers
        self.stickers = self.extract_sticker_info(item_info)
        self.update_stickers_prices()
        self.stickers_price = self.get_stickers_sum_price(self.stickers)

        # Charm
        self.charm = self.extract_charm_info(item_info)
        self.charm_price = self.get_charm_price()

        # Strick
        self.strick = StickerStrick()
        self.strick.update_strick_counter(self.stickers)

    def extract_sticker_info(self, item_info):
        stickers = item_info.get("stickers", [])
        print(stickers)
        return stickers

    def extract_charm_info(self, item_info):
        return item_info.get("charm", {})

    def get_stickers_sum_price(self, stickers):
        return sum(sticker['price'] for sticker in stickers)
