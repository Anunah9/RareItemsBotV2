import re
from bs4 import BeautifulSoup
import requests
from assets.session import SteamSession

class Parser:
    def __init__(self, session: SteamSession):
        self.steam_session: SteamSession = session
        self.req_session: requests.Session = session.get_session()

    def get_items_from_market(self, url):
        response = self.req_session.get(url)

        if response.status_code != 200:
            raise Exception(
                f"Response complete with code error: {response.status_code}"
            )

        soup = BeautifulSoup(response.text)
        items_table = soup.find("div", {"id": "searchResultsRows"})
        items = items_table.find_all("div", id=re.compile(r"listing_\d+"))
        print(items)
        print(len(items))
