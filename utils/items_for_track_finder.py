from pprint import pprint
import requests
import urllib
from urllib.parse import urlunparse
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
from assets.inspect import AsyncItemInfoFetcher, MockItemInfoFetcher, ItemInfoFetcher
from assets.proxy import ProxyManager
from assets.utils import read_json_from_file
from assets.database import Items, SqliteItemsRepository


def get_items_from_file(file_path: str):
    with open(file_path, "r") as f:
        return f.read().split("\n")


def get_all_exterior_for_item(item: str):
    exteriors = ["(Factory New)", "(Minimal Wear)", "(Field-Tested)",
                 "(Well-Worn)", "(Battle-Scarred)"]
    return [" ".join((item, exterior)) for exterior in exteriors]


def build_url(item_name):
    # Returns a list in the structure of urlparse.ParseResult
    base_url = "https://steamcommunity.com/market/listings/730/"
    encoded_item_name = urllib.parse.quote(item_name)

    # Формируем итоговый URL
    return base_url + encoded_item_name


def get_items():
    items = get_items_from_file("./items_raw.txt")
    result = []
    # for item in items:
    # items_with_exterior = get_all_exterior_for_item(item)
    for i in items:
        result.append({i: build_url(i)})
    return result


async def get_steam_session(login, password, mafile):

    steamclient = SteamPyClient()
    steam_session = AsyncSteamSession(steamclient, login, password, mafile)
    # steam_session.login()
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

    item_info_fetcher = ItemInfoFetcher()
    price_repository = PricesRepository("./db.db")
    item_price_fetcher = ItemPriceFetcher(db_repostiotory=price_repository)
    item_price_fetcher.update_all_prices(currency=currency_rates)


async def main():
    items = get_items()
    pprint(items)


if __name__ == "__main__":
    config_json = read_json_from_file("./config.txt")
    API_KEY = config_json.get("API_KEY")
    PARSER_LOGIN = config_json.get("PARSER_LOGIN")
    PARSER_PASSWORD = config_json.get("PARSER_PASSWORD")
    PARSER_MAFILE = config_json.get("PARSER_MAFILE")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
