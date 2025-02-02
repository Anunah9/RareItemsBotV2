from dataclasses import dataclass


@dataclass
class Config:
    strick3: float
    strick45: float
    nostrick: float
    autobuy: bool
    min_stickers_price: float
