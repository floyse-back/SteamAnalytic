import steamspypi
from app.infrastructure.db.models.steam_models import SteamBase, SteamBaseTemp
import time

from app.infrastructure.logger.logger import logger


class SteamParser:
    def __init__(self):
        self.startpage:int = 0
        self.__current_page = self.startpage
        self.__empty_data_score = 0
        self.__count_error = 0
        self.filter_set = set()

    def create_data_list(self,data: dict):
        games = []
        for game_data in data.values():
            if game_data['appid'] not in self.filter_set:
                self.filter_set.add(game_data['appid'])
                game = SteamBaseTemp(
                    appid=str(game_data['appid']),
                    name=str(game_data['name']),
                    developer=str(game_data['developer']),
                    publisher=str(game_data['publisher']),
                    positive=int(game_data['positive']),
                    negative=int(game_data['negative']),
                    average_forever=int(game_data['average_forever']),
                    average_2weeks=int(game_data['average_2weeks']),
                    median_forever=int(game_data['median_forever']),
                    median_2weeks=int(game_data['median_2weeks']),
                    price=int(game_data['price']),
                    discount=int(game_data['discount'])
                )
                games.append(game)
        return games

    @property
    def current_page(self):
        return self.__current_page

    @current_page.setter
    def current_page(self,value):
        self.__current_page = value

    def create_query(self):
        data_dict = dict()
        data_dict['request'] = 'all'
        data_dict['page'] = str(self.current_page)
        return data_dict

    def request_steampipy(self):
        data = steamspypi.download(self.create_query())
        return data

    def page_parse(self,time_sleep_default:int=0,time_sleep_exception:int=0):
        while self.current_page <= 87 or self.__empty_data_score < 5:
            try:
                data = self.request_steampipy()
                if data != {}:
                    self.__empty_data_score = 0
                    new_data = self.create_data_list(data)
                    yield new_data
                elif data == {}:
                    self.__empty_data_score += 1

                time.sleep(time_sleep_default)
            except Exception as ex:
                logger.critical(f"Error info: {ex}")
                time.sleep(time_sleep_exception)
            finally:
                self.current_page += 1
            logger.info(f"Current page: {self.current_page}")



