import asyncio
import os
import time
import aiohttp.client_exceptions
from steampy.guard import generate_one_time_code
import aiohttp
from dotenv import load_dotenv
from assets.currency_rates import Currency
from assets.parser import AsyncParser
from assets.proxy import ProxyManager
from assets.session import AsyncSteamSession, SteamPyClient


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
        raise exc
        # print("Failed to load session. Logging in...")

    steam_session.login()
    print("Login successful. Saving session...")
    steam_session.save_client("./accounts/")
    print("Save successful")
    steam_session.async_session = steam_session.get_async_session()
    return steam_session


async def check_parser(session: AsyncSteamSession, proxy_manager: ProxyManager, i):
    await asyncio.sleep(i)

    url = "https://steamcommunity.com/market/listings/730/AK-47%20|%20Slate%20(Field-Tested)"
    proxy = proxy_manager.get_random_proxy()

    try:
        response = await session.async_session.get(
            url=url, proxy=proxy, ssl=False, timeout=5
        )
        print("------------------------------")
        print(response.status)
        print(i)
    except await aiohttp.client_exceptions.ClientConnectionError:
        print("Превышен таймаут семафора")

    # async with session.get_async_session() as local_session:
    #     print("session: ", await session.is_alive())
    #     response = await local_session.get(url, proxy=proxy)
    #     print(response.status)


async def main():
    session = await get_steam_session()
    print("Проверка сессии: ", session.is_alive())
    proxy_manager = ProxyManager()
    proxy_manager.load_proxies("./proxies.txt")

    tasks = [check_parser(session, proxy_manager, i) for i in range(200)]
    await asyncio.gather(*tasks)


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
