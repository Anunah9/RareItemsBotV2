"""Модуль для покупки предмета"""
from assets.session import AsyncSteamSession
from steampy.models import Currency, GameOptions
from steampy import market


class BuyModule:
    def __init__(self, steam_client: AsyncSteamSession):
        self.steam_session: AsyncSteamSession = steam_client

    def buy_item(self, item_name, market_id, price, fee):
        client = self.steam_session.get_client()
        client.market.buy_item(item_name, market_id, price, fee, game=GameOptions.CS,
                               currency=Currency.RUB)
