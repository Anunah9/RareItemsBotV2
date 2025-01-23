from assets.steamapi import SteamBot, SteamSession


## TODO Сделать файл конфигурации
if __name__ == "__main__":
    steam_session = SteamSession("arinugraha31", "arinugraha123")
    steam_session.login()
    bot = SteamBot(steam_session)
    bot.start()
