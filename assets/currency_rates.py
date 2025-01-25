import requests


class Currency:
    rates_ids = {
        1: "USD",
        2: "GBP",
        3: "EUR",
        4: "CHF",
        5: "RUB",
        6: "PLN",
        7: "BRL",
        8: "JPY",
        9: "NOK",
        10: "IDR",
        11: "MYR",
        12: "PHP",
        13: "SGD",
        14: "THB",
        15: "VND",
        16: "KRW",
        17: "TRY",
        18: "UAH",
        19: "MXN",
        20: "CAD",
        21: "AUD",
        22: "NZD",
        23: "CNY",
        24: "INR",
        25: "CLP",
        26: "PEN",
        27: "COP",
        28: "ZAR",
        29: "HKD",
        30: "TWD",
        31: "SAR",
        32: "AED",
        33: "SEK",
        34: "ARS",
        35: "ILS",
        36: "BYN",
        37: "KZT",
        38: "KWD",
        39: "QAR",
        40: "CRC",
        41: "UYU",
    }

    def __init__(self, api_key, default_currency=5):
        self.api_key = api_key
        self.rates: dict | None = None
        self.DEFAULT_CURRENCY = 5

    def change_currency(
        self, price, start_currency_id: int, target_currency_id: int = -1
    ):
        """Convert price for target currency. If target not provided convert to DEFAULT_CURRENCY by defalt."""
        if target_currency_id == -1:
            target_currency_id = self.DEFAULT_CURRENCY
        # Остаток от деление на 100 так как изначально currency id приходит в виде 20xx
        start_currency_definition = self.rates_ids[start_currency_id % 100]
        target_currency_definition = self.rates_ids[target_currency_id % 100]
        start_currency_value = self.rates[start_currency_definition]
        target_currency_value = self.rates[target_currency_definition]
        currency = target_currency_value / start_currency_value
        return price * currency

    def update_steam_currency_rates(
        self,
    ):
        """Обновляет куры валют на актуальные. (Пока что вызов этой функции обязателен перд использоавнием)"""
        params = {
            "key": self.api_key,
            "format": "json",
            "amp": "",
            "appid": "1764030",
        }
        url = f"https://api.steampowered.com/ISteamEconomy/GetAssetPrices/v1/"
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(
                f"Request completed with error code: {response.status_code}"
            )
        elif response.json()["result"]["success"] == True:
            self.rates = response.json()["result"]["assets"][0]["prices"]
