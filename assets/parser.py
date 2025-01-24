from bs4 import BeautifulSoup
from assets.currency_rates import Currency
from assets.session import SteamSession
import json
from pprint import pprint


class Parser:
    def __init__(self, session: SteamSession, currency: Currency):
        self.steam_session: SteamSession = session
        self.currency: Currency = currency

    def get_json_items_from_market(self, url: str) -> dict:
        response = self.steam_session.session.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Response complete with code error: {response.status_code}"
            )
        soup = BeautifulSoup(response.text, "lxml")
        items_table = soup.findAll("script", {"type": "text/javascript"})
        items = str(items_table[-1]).split("var g_rgListingInfo = ")[1].split(";")[0]
        return json.loads(items)

    def calculate_price(self, item_data: dict) -> float:
        price_no_fee = int(item_data.get("price", 0))
        fee = int(item_data.get("fee", 0))
        currency_id = item_data.get("currencyid")
        if currency_id is None:
            raise ValueError("Missing currency_id in item data")
        price = (price_no_fee + fee) / 100
        return self.currency.change_currency(price, currency_id)

    def construct_inspect_link(self, item_data: dict, listing_id: str) -> str:
        raw_inspect_link = item_data.get("asset").get("market_actions")[0].get("link")
        asset_id = item_data.get("asset").get("id")
        return raw_inspect_link.replace("listingid", listing_id).replace(
            "assetid", asset_id
        )

    def extract_item_data(self, items_json: dict) -> list[dict]:
        extracted_items = []
        for listing_id, item_data in items_json.items():
            inspect_link = self.construct_inspect_link(item_data, listing_id)
            price = self.calculate_price(item_data)
            extracted_items.append(
                {
                    "listing_id": listing_id,
                    "inspect_link": inspect_link,
                    "price": price,
                }
            )
        return extracted_items
