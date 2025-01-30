import os
import pickle
from steampy.client import SteamClient
import requests
from typing import Protocol
from aiohttp.client import ClientSession


class ISteamSession(Protocol):
    def login(self, username, password):
        pass

    def save_cookies_session(self, path):
        pass

    def load_cookie_session(self, path):
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

    def is_alive(self):
        return self._client.is_session_alive()


class SteamSession(ISteamSession):
    def __init__(self, client: ISteamClient, username, password, path_to_mafile):
        self.client = client
        self.session = None
        self.username = username
        self.password = password
        self.path_to_mafile = path_to_mafile

    def login(self):
        self.client.login(self.username, self.password, self.path_to_mafile)

    def get_session(self):
        return self.client.get_session()

    def save_cookies_session(self, path):
        # Сохранение cookie в файл
        res_path = os.path.join(path, self.username)
        with open(res_path, "wb") as f:
            pickle.dump(self.session, f)

    def save_client(self, path):
        # Сохранение клиента SteamPy в файл
        res_path = os.path.join(path, self.username + "_client")
        with open(res_path, "wb") as f:
            pickle.dump(self.client, f)

    def load_cookie_session(self, path):
        # Загрузка cookie из файла
        res_path = os.path.join(path, self.username)
        if self.username not in os.listdir(path):
            raise Exception("No file for load. Try save_session first.")
        with open(res_path, "rb") as f:
            self.session = pickle.load(f)

    def load_client(self, path):
        # Загрузка клиента SteamPy из файла
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


class AsyncSteamSession(ISteamSession):
    def __init__(
        self, client: ISteamClient, username: str, password: str, path_to_mafile: str
    ):
        self.client: SteamPyClient = client
        self.sync_session: requests.Session
        self.async_session: ClientSession
        self.username = username
        self.password = password
        self.path_to_mafile = path_to_mafile

    def login(self):
        self.client.login(self.username, self.password, self.path_to_mafile)

    def get_async_session(self):
        # Можете передать заголовки из вашей существующей сессии
        headers = {
            "Host": "steamcommunity.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "DNT": "1",
            "Sec-GPC": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Priority": "u=0, i",
        }
        cookie_jar = self.client.get_session().cookies
        return ClientSession(
            headers=headers, cookies=cookie_jar.get_dict("steamcommunity.com")
        )

    def get_session(self):
        return self.client.get_session()

    def save_cookies_session(self, path):
        # Сохранение cookie в файл
        res_path = os.path.join(path, self.username)
        with open(res_path, "wb") as f:
            pickle.dump(self.session, f)

    def save_client(self, path):
        # Сохранение клиента SteamPy в файл
        res_path = os.path.join(path, self.username + "_client")
        with open(res_path, "wb") as f:
            pickle.dump(self.client, f)

    def load_cookie_session(self, path):
        # Загрузка cookie из файла

        res_path = os.path.join(path, self.username)
        if self.username not in os.listdir(path):
            raise Exception("No file for load. Try save_session first.")
        with open(res_path, "rb") as f:
            self.session = pickle.load(f)

    def load_client(self, path):
        # Загрузка клиента SteamPy из файла
        res_path = os.path.join(path, self.username + "_client")
        print(res_path)
        if self.username + "_client" not in os.listdir(path):
            raise Exception("No file for load. Try save_session first.")
        with open(res_path, "rb") as f:
            self.client = pickle.load(f)

    def is_alive(self):
        # Проверка активности сессии
        # url = "https://steamcommunity.com/market/"
        # response = await self.async_session.get(url)
        # return self.username in await response.text()
        return self.client.is_alive()
