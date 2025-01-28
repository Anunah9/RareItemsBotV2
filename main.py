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

# Загрузка переменных окружения
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


async def get_steam_session():
    steamclient = SteamPyClient()
    steam_session = AsyncSteamSession(
        steamclient, "arinugraha31", "arinugraha123")

    try:
        steam_session.load_session("./accounts/")
        steam_session.convert_sync_to_async_session()
        if await steam_session.is_alive():
            print("Successfully loaded session")
            return steam_session
    except:
        print("Failed to load session. Logging in...")

    steam_session.login()
    print("Login successful. Saving session...")
    steam_session.save_session("./accounts/")
    print("Save successful")
    steam_session.convert_sync_to_async_session()
    return steam_session


async def create_bot():
    steam_session = await get_steam_session()
    currency_rates = Currency(API_KEY)
    currency_rates.update_steam_currency_rates()
    parser = AsyncParser(steam_session, currency_rates)

    # item_info_fetcher = MockItemInfoFetcher()
    # item_price_fetcher = MockItemPriceFetcher()

    item_info_fetcher = ItemInfoFetcher()

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
    API_KEY = os.getenv("API_KEY")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
