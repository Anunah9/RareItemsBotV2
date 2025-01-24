from assets.session import SteamSession
from assets.bot import SteamBot
from assets.currency_rates import Currency
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

if __name__ == "__main__":
    API_KEY = os.getenv("API_KEY")
    steam_session = SteamSession("arinugraha31", "arinugraha123")
    try:
        steam_session.load_session("./accounts/")
    except:
        steam_session.login()
        print("Login successful. Saving session...")
        steam_session.save_session("./accounts/")
        print("Save successfull")
    else:
        if steam_session.is_alive():
            print("Successful loaded session")

    currency_rates = Currency(API_KEY)
    currency_rates.update_steam_currency_rates()
    print(currency_rates.rates)
    example = currency_rates.change_currency(2781, 2023)
    print(example)
    bot = SteamBot(steam_session)
    bot.start()
