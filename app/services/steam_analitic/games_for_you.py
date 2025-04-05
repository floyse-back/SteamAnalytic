from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.analitic_repository import AnaliticRepository
from app.models.steam import Game

class GamesForYou:
    def __init__(self):
        self.repository = AnaliticRepository()

    async def find_games_for_you(self,data:dict,session:AsyncSession):
        appid_list = self.__get_games_appid_list(data)
        games_details_list = await self.repository.get_games_for_appids(session,appid_list)
        data = self.__count_games_elements(games_details_list)

        elements_data = await self.repository.find_games_for_elements(genre_weights=self.ganres,category_weights=self.categories,session=session,limit=10)

        return elements_data

    def __get_games_appid_list(self,data:dict):
        add_rank_data = self.__add_rank_data(data.get("games"))
        return add_rank_data

    def __add_rank_data(self,data:list)->list:
        sorted_data = sorted(data, key= lambda x:x.get("playtime_forever"),reverse=True)
        appid_games = []
        for index,game in enumerate(sorted_data):
            if game.get("playtime_forever")!=0:
                appid_games.append(int(game.get("appid")))

        return appid_games

    def __count_games_elements(self,game_data:list[Game]):
        self.ganres = dict()
        self.publishers = dict()
        self.categories = dict()
        for game in game_data:
            self.__count_ganres(game)
            self.__count_publishers(game)
            self.__count_categories(game)

        self.ganres = self.__resize_elements(self.ganres)
        self.publishers = self.__resize_elements(self.publishers)
        self.categories = self.__resize_elements(self.categories)

        return {
            "ganres_dict":self.ganres,
            "publishers_dict":self.publishers,
            "categories_dict":self.categories,
        }


    def __count_ganres(self,game):
        for ganre in game.game_ganre:
            ganre_name = ganre.ganres_name
            if self.ganres.get(ganre_name):
                self.ganres[ganre_name] += 1
            else:
                self.ganres[ganre_name] = 1

    def __count_publishers(self,game):
        for publisher in game.game_publisher:
            publisher_name = publisher.publisher_name
            if self.publishers.get(publisher_name):
                self.publishers[publisher_name] += 1
            else:
                self.publishers[publisher_name] = 1

    def __count_categories(self,game):
        for category in game.game_categories:
            categories_name = category.category_name
            if self.categories.get(categories_name):
                self.categories[categories_name] += 1
            else:
                self.categories[categories_name] = 1

    def __resize_elements(self,data:dict,elements:int = 5):
        items = data.items()
        items = sorted(items,key= lambda x:x[1],reverse=True)
        return items[:elements]


