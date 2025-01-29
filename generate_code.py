import asyncio
import os
import time
from steampy.guard import generate_one_time_code
import aiohttp
from dotenv import load_dotenv
from assets.currency_rates import Currency
from assets.parser import AsyncParser
from assets.proxy import ProxyManager
from assets.session import AsyncSteamSession, SteamPyClient


async def create_test_bot():

    client = SteamPyClient()
    print(PARSER_LOGIN, PARSER_PASSWORD, PARSER_MAFILE)
    session = AsyncSteamSession(
        client,
        username=PARSER_LOGIN,
        password=PARSER_PASSWORD,
        path_to_mafile=PARSER_MAFILE,
    )

    session.login()
    session.load_session("./accounts/")
    session.async_session = session.get_async_session()
    print("Проверка сессии: ", session.is_alive())
    # currency_rates = Currency(API_KEY)
    # currency_rates.update_steam_currency_rates()
    return session


async def check_parser(session: AsyncSteamSession, proxy_manager: ProxyManager, i):
    await asyncio.sleep(i)
    print(i)
    url = "https://steamcommunity.com/market/listings/730/AK-47%20|%20Slate%20(Field-Tested)"
    proxy = proxy_manager.get_random_proxy()

    response = await session.async_session.get(url=url, proxy=proxy, ssl=False)
    print(response.status)

    # async with session.get_async_session() as local_session:
    #     print("session: ", await session.is_alive())
    #     response = await local_session.get(url, proxy=proxy)
    #     print(response.status)


async def main():
    session = await create_test_bot()
    proxy_manager = ProxyManager()
    proxy_manager.load_proxies("./proxies.txt")
    print(time.time())
    print(generate_one_time_code("HJXEBEq1x7L7EzFjFFUHrJ/5NQw=", int(time.time())))
    # tasks = [check_parser(session, proxy_manager, i) for i in range(200)]
    # await asyncio.gather(*tasks)


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
