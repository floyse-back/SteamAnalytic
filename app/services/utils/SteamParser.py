import steamspypi
from ...database.models import SteamBase
import time

class SteamParser:
    def __init__(self):
        self.startpage:int = 0
        self.__current_page = self.startpage
        self.__empty_data_score = 0

    @staticmethod
    def create_data_list(data: dict):
        games = []
        for game_data in data.values():
            game = SteamBase(
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
        print(data_dict)
        return data_dict

    def request_steampipy(self):
        data = steamspypi.download(self.create_query())
        return data

    def page_parse(self):
        while self.current_page <80 and self.__empty_data_score < 3:
            data = self.request_steampipy()
            if data != {}:
                self.__empty_data_score = 0
                new_data = self.create_data_list(data)
                yield new_data
            elif data == {}:
                print("Empty data")
                print(data)
                self.__empty_data_score += 1

            self.current_page += 1
            time.sleep(70)

            print(f"Empty data score: {self.__empty_data_score}")
            print(f"Current page: {self.current_page}")



