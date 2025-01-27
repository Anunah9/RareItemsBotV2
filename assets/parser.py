from bs4 import BeautifulSoup
from assets.currency_rates import Currency
from assets.session import SteamSession
import json
from pprint import pprint
from assets.utils import construct_inspect_link


class Parser:
    def __init__(self, session: SteamSession, currency: Currency):
        self.steam_session: SteamSession = session
        self.currency: Currency = currency

    def get_raw_data_from_market(self, url: str) -> str:
        """Возвраает сырые json даные о списке лотов с ТП"""
        response = self.steam_session.session.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Response complete with code error: {response.status_code}"
            )
        return response.text

    def extract_json_from_raw_data(self, raw_data: str):
        soup = BeautifulSoup(raw_data, "lxml")
        items_table = soup.findAll("script", {"type": "text/javascript"})
        items = str(items_table[-1]).split("var g_rgListingInfo = ")[1].split(";")[0]

        return json.loads(items)

    def calculate_price(self, item_data: dict) -> float:
        """Вычисляет полную цену предмета (цена без комиссии + комиссия) в рублях"""
        price_no_fee = int(item_data.get("price", 0))
        fee = int(item_data.get("fee", 0))
        currency_id = item_data.get("currencyid")  # id валюты предмета.
        if currency_id is None:
            raise ValueError("Missing currency_id in item data")
        price = (price_no_fee + fee) / 100
        return self.currency.change_currency(price, currency_id)

    def extract_item_data(self, items_json: dict) -> list[dict]:
        """Формирует список данных о предметах."""
        extracted_items = []
        for listing_id, item_data in items_json.items():
            inspect_link = construct_inspect_link(item_data, listing_id)
            price = self.calculate_price(item_data)
            extracted_items.append(
                {
                    "listing_id": listing_id,
                    "inspect_link": inspect_link,
                    "price": price,
                }
            )
        return extracted_items
