import os
import pickle
from steampy.client import SteamClient
import requests
from typing import Protocol
from aiohttp.client import ClientSession


class ISteamSession(Protocol):
    def login(self, username, password):
        pass

    def save_session(self, path):
        pass

    def load_session(self, path):
        pass

    def is_alive(self):
        pass


class ISteamClient(Protocol):
    def login(self, username, password, steam_guard_file):
        pass

    def get_session(self):
        pass


class SteamPyClient(ISteamClient):
    def __init__(self):
        self._client = None

    def login(self, username, password, steam_guard_file):
        from steampy.client import SteamClient

        self._client = SteamClient("", username, password)
        self._client.login(username, password, steam_guard_file)

    def get_session(self):
        return self._client._session


class SteamSession(ISteamSession):
    def __init__(self, client: ISteamClient, username, password):
        self.client = client
        self.session = None
        self.username = username
        self.password = password

    def login(self):
        self.client.login(self.username, self.password,
                          "./fake_steam_guard.txt")
        self.session = self.client.get_session()

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
        return self.username in response.text
