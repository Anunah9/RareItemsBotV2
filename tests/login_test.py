from steampy.client import SteamClient

API = "2BDF631FB91A0A9357B0EE2AB15AF479"
PARSER_LOGIN = "enduringlegisla"
PARSER_PASSWORD = "UYLtVO0PvUz9X"
PARSER_MAFILE = "../accounts/maFiles/enduringlegisla.txt"
client = SteamClient(API, PARSER_LOGIN, PARSER_PASSWORD, PARSER_MAFILE)
client.login(PARSER_LOGIN, PARSER_PASSWORD, PARSER_MAFILE)
