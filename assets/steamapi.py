from steampy.client import SteamClient
from steampy.login import InvalidCredentials, LoginExecutor
import requests
from bs4 import BeautifulSoup


class ISteamSession:
    def login(self, username, password):
        pass

    def save_session(self, path):
        pass

    def load_session(self, path):
        pass

    def is_alive(self):
        pass


class SteamSession(ISteamSession):
    def __init__(self, username, password):
        # TODO Передавать эти данные в файле конфигурации
        self.fake_steam_guard_file = "./fake_steam_guard.txt"
        self.username, self.password = username, password
        self.steam_client = SteamClient("", self.username, self.password)

    def login(self):
        print(self.username, self.password)
        self.steam_client.login(
            self.username, self.password, self.fake_steam_guard_file
        )

    def get_session(self) -> requests.Session:
        return self.steam_client._session

    def save_session(self):
        # Сохранение сессии
        pass

    def load_session(self):
        # Загрузка сессии
        pass

    def is_alive(self):
        # Проверка активности сессии
        url = "https://steamcommunity.com/market/"
        session = self.get_session()
        response = session.get(url)
        if response.text.find(self.username) > 0:
            return True
        else:
            return False


class Parser:
    def __init__(self, session: SteamSession):
        self.steam_session: SteamSession = session
        self.req_session: requests.Session = session.get_session()

    def get_items_from_market(self, url):
        response = self.req_session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text)
            print(soup)
        else:
            raise Exception(
                f"Response complete with code error: {response.status_code}"
            )


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
