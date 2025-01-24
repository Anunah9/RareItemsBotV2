from bs4 import BeautifulSoup
from assets.currency_rates import Currency
from assets.session import SteamSession
import json
from pprint import pprint


class Parser:
    def __init__(self, session: SteamSession, currency: Currency):
        self.steam_session: SteamSession = session
        self.currency: Currency = currency

    def get_json_items_from_market(self, url):
        response = self.steam_session.session.get(url)

        if response.status_code != 200:
            raise Exception(
                f"Response complete with code error: {response.status_code}"
            )
        soup = BeautifulSoup(response.text, "lxml")
        items_table = soup.findAll("script", {"type": "text/javascript"})
        items = str(items_table[-1]).split("var g_rgListingInfo = ")[1].split(";")[0]
        items_to_json = json.loads(items)
        return items_to_json

    def extract_item_data(self, items_json):
        extracted_items = []
        for listing_id, item_data in items_json.items():
            item_name = item_data.get("name", "Unknown")
            price = item_data.get("price", "Unknown")
            extracted_items.append(
                {"listing_id": listing_id, "name": item_name, "price": price}
            )
        return extracted_items
