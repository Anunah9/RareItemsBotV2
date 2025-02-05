import asyncio

from assets.inspect import ItemInfoFetcher


inspect = ItemInfoFetcher()


def get_info():
    data = inspect.get_sticker_and_charm_info(
        'steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198187797831A41756671076D5389858913359538555')
    print(data)


get_info()
