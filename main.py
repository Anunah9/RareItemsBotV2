import asyncio
import json
from assets.buy import BuyModule
from assets.config import Config
from assets.parser import AsyncParser
from assets.prices import ItemPriceFetcher, MockItemPriceFetcher, PricesRepository
from assets.session import AsyncSteamSession, SteamPyClient
from assets.bot import AsyncSteamBot, SteamBot
from assets.currency_rates import Currency
import os
from dotenv import load_dotenv
from assets.inspect import MockItemInfoFetcher, ItemInfoFetcher
from assets.proxy import ProxyManager
from assets.utils import read_json_from_file
from assets.database import Items, SqliteItemsRepository

# Загрузка переменных окружения


async def get_steam_session(login, password, mafile):
    print(login, password, mafile)
    steamclient = SteamPyClient()
    steam_session = AsyncSteamSession(steamclient, login, password, mafile)

    try:
        steam_session.load_client("./accounts/")
        steam_session.async_session = steam_session.get_async_session()
        if steam_session.is_alive():
            print("Successfully loaded session")
            return steam_session
    except Exception as exc:
        # raise exc
        print("Failed to load session. Logging in...")

    steam_session.login()
    print("Login successful. Saving session...")
    steam_session.save_client("./accounts/")
    print("Save successful")
    steam_session.async_session = steam_session.get_async_session()
    return steam_session


async def create_bot():
    steam_session_parser = await get_steam_session(
        PARSER_LOGIN, PARSER_PASSWORD, PARSER_MAFILE
    )
    currency_rates = Currency(API_KEY)
    currency_rates.update_steam_currency_rates()

    proxy_manager = ProxyManager()
    proxy_manager.load_proxies("./proxies.txt")
    parser = AsyncParser(
        steam_session_parser, currency_rates, proxy_manager=proxy_manager
    )

    item_info_fetcher = MockItemInfoFetcher()
    item_price_fetcher = MockItemPriceFetcher()

    # item_info_fetcher = ItemInfoFetcher()

    price_repository = PricesRepository("./db.db")
    item_price_fetcher = ItemPriceFetcher(db_repostiotory=price_repository)
    item_price_fetcher.update_all_prices(currency=currency_rates)

    config = Config(STRICK3, STRICK45, NOSTRICK, AUTOBUY)

    stema_client_buyer = await get_steam_session(
        BUYER_LOGIN, BUYER_PASSWORD, BUYER_MAFILE
    )
    items_repository = SqliteItemsRepository("./db.db")
    items = Items(items_repository)

    buy_module = BuyModule(stema_client_buyer)
    return AsyncSteamBot(
        steam_session_parser,
        parser,
        item_info_fetcher,
        item_price_fetcher,
        config,
        buy_module,
        items,
    )


async def main():
    bot = await create_bot()
    await bot.start()


if __name__ == "__main__":
    config_json = read_json_from_file("./config.txt")
    API_KEY = config_json.get("API_KEY")
    PARSER_LOGIN = config_json.get("PARSER_LOGIN")
    PARSER_PASSWORD = config_json.get("PARSER_PASSWORD")
    PARSER_MAFILE = config_json.get("PARSER_MAFILE")

    BUYER_LOGIN = config_json.get("BUYER_LOGIN")
    BUYER_PASSWORD = config_json.get("BUYER_PASSWORD")
    BUYER_MAFILE = config_json.get("BUYER_MAFILE")

    STRICK3 = float(config_json.get("STRICK3"))
    STRICK45 = float(config_json.get("STRICK45"))
    NOSTRICK = float(config_json.get("NOSTRICK"))
    AUTOBUY = bool(int(config_json.get("AUTOBUY")))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
