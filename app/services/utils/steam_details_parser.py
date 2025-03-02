import time
from steam_web_api import Steam

STEAM_API_KEY = "7D6845B4F967206A190384C179FA1065"

class SteamDetailsParser:
    def __init__(self,game_list):
        self.steam = Steam(STEAM_API_KEY)
        self.game_list_appid = game_list
        self.filters = 'basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,movies,recommendations,achievements'

    def parse(self):
        new_list = []
        for i in self.game_list_appid:
            result = self.steam.apps.get_app_details(int(i),filters=self.filters)
            new_list.append(result)
            time.sleep(1)

        return new_list

st_det = ["570",'1238840']
test = SteamDetailsParser(st_det)
print(test.parse())