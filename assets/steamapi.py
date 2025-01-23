from assets.parser import Parser
from assets.session import ISteamSession


class SteamBot:
    def __init__(self, session: ISteamSession):
        self.session = session

    def start(self):
        if self.session.is_alive():
            print("Bot started with an active session.")
            parser = Parser(self.session)
            item_url = "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20(Field-Tested)"
            items = parser.get_items_from_market(item_url)

        # Основная логика бота
