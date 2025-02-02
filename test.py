import asyncio
from assets.inspect import AsyncItemInfoFetcher


inspect = AsyncItemInfoFetcher()


async def get_info():
    data = await inspect.get_sticker_and_charm_info('steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M659316018227598623A41559919247D3072130084370312059')
    print(data)


loop = asyncio.get_event_loop()
loop.run_until_complete(get_info())
