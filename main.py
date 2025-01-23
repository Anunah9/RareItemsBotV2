from assets.session import SteamSession
from assets.steamapi import SteamBot


## TODO Сделать файл конфигурации
if __name__ == "__main__":
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

    bot = SteamBot(steam_session)
    bot.start()
