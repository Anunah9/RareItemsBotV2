import asyncio
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

# Загрузка переменных окружения


async def get_steam_session():
    steamclient = SteamPyClient()
    steam_session = AsyncSteamSession(
        steamclient, PARSER_LOGIN, PARSER_PASSWORD, PARSER_MAFILE
    )

    try:
        steam_session.load_cookie_session("./accounts/")
        steam_session.async_session = steam_session.get_async_session()
        if steam_session.is_alive():
            print("Successfully loaded session")
            return steam_session
    except:
        print("Failed to load session. Logging in...")

    steam_session.login()
    print("Login successful. Saving session...")
    steam_session.save_cookies_session("./accounts/")
    print("Save successful")
    steam_session.async_session = steam_session.get_async_session()
    return steam_session


async def create_bot():
    steam_session = await get_steam_session()
    currency_rates = Currency(API_KEY)
    currency_rates.update_steam_currency_rates()

    proxy_manager = ProxyManager()
    proxy_manager.load_proxies("./proxies.txt")
    parser = AsyncParser(steam_session, currency_rates, proxy_manager=proxy_manager)

    item_info_fetcher = MockItemInfoFetcher()
    # item_price_fetcher = MockItemPriceFetcher()

    # item_info_fetcher = ItemInfoFetcher()

    price_repository = PricesRepository("./db.db")
    item_price_fetcher = ItemPriceFetcher(db_repostiotory=price_repository)
    item_price_fetcher.update_all_prices(currency=currency_rates)

    strick3 = float(os.getenv("STRICK3"))
    strick45 = float(os.getenv("STRICK45"))
    nostrick = float(os.getenv("NOSTRICK"))
    config = Config(strick3, strick45, nostrick)
    return AsyncSteamBot(
        steam_session, parser, item_info_fetcher, item_price_fetcher, config
    )


async def main():
    bot = await create_bot()
    await bot.start()


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
