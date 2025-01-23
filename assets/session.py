import os
import pickle
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
        self.session: requests.Session | None = None

    def login(self):
        print(self.username, self.password)
        steam_client = SteamClient("", self.username, self.password)
        steam_client.login(self.username, self.password, self.fake_steam_guard_file)
        self.session = steam_client._session

    def save_session(self, path):
        # Сохранение сессии
        res_path = os.path.join(path, self.username)
        with open(res_path, "wb") as f:
            pickle.dump(self.session, f)

    def load_session(self, path):
        # Загрузка сессии
        res_path = os.path.join(path, self.username)
        if self.username not in os.listdir(path):
            raise Exception("No file for load. Try save_session first.")
        with open(res_path, "rb") as f:
            self.session = pickle.load(f)

    def is_alive(self):
        # Проверка активности сессии
        url = "https://steamcommunity.com/market/"
        response = self.session.get(url)
        if response.text.find(self.username) > 0:
            return True
        else:
            return False
