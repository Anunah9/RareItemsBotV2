from dataclasses import dataclass

from assets.inspect import IItemInfoFetcher
from assets.prices import IItemPriceFetcher


class StickerStrick:
    strick: bool
    sticker_name: str
    single_sticker_price: float
    sum_price_strick: float

    def update_strick_counter(self, stickers):
        strick_dict = {}
        for sticker in stickers:
            if sticker.get("name") not in strick_dict:
                strick_dict[sticker["name"]] = 1
            else:
                strick_dict[sticker["name"]] += 1

        strick = list(filter(
            lambda x: x[1] >= 3, strick_dict.items()))
        print(strick)
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
        item_info = self.itemInfoFetcher.get_sticker_and_charm_info(
            self.inspect_link)
        self.stickers = self.extract_sticker_info(item_info)
        self.update_stickers_prices()
        self.stickers_price = self.get_stickers_sum_price(self.stickers)
        self.charm = self.extract_charm_info(item_info)
        self.charm_price = self.get_charm_price()
        self.strick = StickerStrick()
        self.strick.update_strick_counter(self.stickers)

    def extract_sticker_info(self, item_info):
        return item_info.get("stickers", [])

    def extract_charm_info(self, item_info):
        return item_info.get("charm", {})

    def get_stickers_sum_price(self, stickers):
        return sum(sticker['price'] for sticker in stickers)
