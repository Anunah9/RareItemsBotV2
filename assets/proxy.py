from os import PathLike

import random
from typing import Protocol


class IProxyManager(Protocol):
    def load_proxies(self, path: PathLike):
        pass

    def get_random_proxy(self):
        pass


class ProxyManager(IProxyManager):
    def __init__(self):
        self.proxies: list

    def load_proxies(self, path):
        with open(path, "r") as f:
            self.proxies = f.readlines()

    def get_random_proxy(self):
        return "http://" + random.choice(self.proxies)
