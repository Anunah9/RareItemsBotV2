import asyncio
from pprint import pprint

from dotenv import load_dotenv
# from assets.currency_rates import Currency
from assets.parser import AsyncParser
from assets.proxy import ProxyManager
from assets.session import AsyncSteamSession, SteamPyClient
from assets.buy import BuyModule
import os
from steampy.client import SteamClient
from steampy.models import GameOptions, Currency


async def get_steam_session():
    steamclient = SteamPyClient()
    steam_session = AsyncSteamSession(
        steamclient, PARSER_LOGIN, PARSER_PASSWORD, PARSER_MAFILE
    )

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


async def main():
    steam_session = await get_steam_session()
    buy_module = BuyModule(steam_client=steam_session)
    proxy_manager = ProxyManager()
    proxy_manager.load_proxies('proxies.txt')
    parser = AsyncParser(steam_session, "",  proxy_manager)

    item_name = "R8 Revolver | Bone Mask (Battle-Scarred)"
    url = r"https://steamcommunity.com/market/listings/730/R8%20Revolver%20%7C%20Bone%20Mask%20(Battle-Scarred)"

    raw_data = await parser.get_raw_data_from_market(url=url)
    data = parser.extract_json_from_raw_data(raw_data=raw_data)
    items = parser.extract_item_data(data)
    item = items[0]
    listing_id = item["listing_id"]
    price = int(item['price'])
    fee = int(item['fee'])
    pprint(item)
    print(price)
    print(fee)

    buy_module.buy_item(item_name, listing_id,
                        price, fee)

    # client = SteamClient(API_KEY, PARSER_LOGIN, PARSER_PASSWORD, PARSER_MAFILE)
    # client.login(PARSER_LOGIN, PARSER_PASSWORD, PARSER_MAFILE)

    # client.market.buy_item(item_name, str(listing_id),
    #                        price, fee,  GameOptions.CS, Currency.RUB)

if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    API_KEY = os.getenv("API_KEY")
    PARSER_LOGIN = os.getenv("PARSER_LOGIN")
    PARSER_PASSWORD = os.getenv("PARSER_PASSWORD")
    PARSER_MAFILE = os.getenv("PARSER_MAFILE")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
