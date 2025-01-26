from dataclasses import dataclass


@dataclass
class StickerStrick:
    sticker_name: str
    sticker_count: int
    sticker_price: float


@dataclass
class ItemData:
    item_name: str
    listing_id: str
    inspect_link: str
    item_price: float
    stickers: list[dict]
    stickers_price: float
    charm: dict
    charm_price: float
    strick: StickerStrick
