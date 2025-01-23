from steampy.client import SteamClient
import requests



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