from assets.parser import Parser
from assets.session import ISteamSession
from pprint import pprint


class SteamBot:
    def __init__(self, session: ISteamSession):
        self.session = session

    def start(self):
        if self.session.is_alive():
            print("Bot started with an active session.")
            parser = Parser(self.session)
            item_url = "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20(Field-Tested)"
            json_data = parser.get_json_items_from_market(item_url)
            pprint(json_data)
            items = parser.extract_item_data(json_data)

        # Основная логика бота
