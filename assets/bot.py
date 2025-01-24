from assets.parser import Parser
from assets.session import ISteamSession
from assets.currency_rates import Currency
from pprint import pprint


class SteamBot:
    def __init__(self, session: ISteamSession, parser: Parser):
        self.session = session
        self.parser = parser

    def start(self):
        if self.session.is_alive():
            print("Bot started with an active session.")

            item_url = "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20(Field-Tested)"
            json_data = self.parser.get_json_items_from_market(item_url)
            # pprint(json_data)
            items = self.parser.extract_item_data(json_data)
            pprint(items)

        # Основная логика бота
