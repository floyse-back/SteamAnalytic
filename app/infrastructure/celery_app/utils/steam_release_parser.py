import time

import httpx
from bs4 import BeautifulSoup

from app.domain.logger import ILogger


class SteamGamesParser:
    def __init__(self,logger:ILogger,url:str='https://store.steampowered.com/search/?sort_by=Released_DESC&ignore_preferences=1&os=win&filter=popularnew&ndl=1'):
        self.logger = logger
        self.URL = url

    def get_url_info(self):
        retry = 0
        while retry < 3:
            retry += retry
            response = httpx.get(self.URL,headers={"User-Agent":"Mozilla/5.0"})
            if response.status_code != 200:
                retry = retry - 1
                time.sleep(retry * 5)
                continue
            else:
                return response.text
        return None

    def execute(self):
        data = self.get_url_info()
        result = list()
        soup = BeautifulSoup(data, "html.parser")
        games_list_div = soup.find("div",class_="search_results")
        self.logger.info(f"{soup.text}")
        if games_list_div is None:
            self.logger.warning("SteamReleaseParser: No search_result_container")
            return "Bad Request"
        list_games_divs = games_list_div.find_all("a")
        self.logger.debug(f"SteamReleaseParser List_Games_Divs: {list_games_divs}")
        for game in list_games_divs:
            appid = game.get("data-ds-appid")
            self.logger.info(f"Appid Game {appid}")
            if not appid is None and appid.isdigit():
                result.append(appid)

        return result

