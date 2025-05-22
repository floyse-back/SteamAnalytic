import datetime
import time
from steam_web_api import Steam
from app.infrastructure.db.models.steam_models import Game, Category, Ganres, Publisher
from app.utils.config import STEAM_API_KEY


class SteamDetailsParser:
    def __init__(self, session):
        self.steam = Steam(STEAM_API_KEY)
        self.filters = 'basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,recommendations,achievements'
        self.session = session

    @staticmethod
    def steam_id_unique(session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return False
        else:
            return True

    @staticmethod
    def get_or_create(session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.flush()  # Ensure the instance is saved to the database and gets an ID
            return instance

    def update_game_details(self, game, existing_game):
        """Функція для оновлення деталей гри."""
        existing_game.is_free = game.get("is_free")
        existing_game.name = game.get("name")
        existing_game.short_description = game.get("short_description")
        existing_game.requirements = game.get("steam_requirements")
        existing_game.initial_price = game.get("price_overview", {}).get("initial", 0)
        existing_game.final_price = game.get("price_overview", {}).get("final", 0)
        existing_game.final_formatted_price = game.get("price_overview", {}).get("final_formatted", "Free")
        existing_game.discount = game.get("price_overview", {}).get("discount_percent", 0)
        existing_game.metacritic = game.get("metacritic", {}).get("score", -1)
        existing_game.achievements = game.get("achievements", {}).get("highlighted", {})
        existing_game.recomendations = int(game.get("recommendations", {}).get("total", 0))
        existing_game.img_url = game.get("capsule_image")
        existing_game.last_updated = datetime.datetime.today().date()

        # Оновлення категорій, жанрів та видавців
        existing_game.game_categories = []
        if game.get("categories"):
            for category in game.get("categories"):
                category_name = category.get("description")
                existing_game.game_categories.append(self.get_or_create(session=self.session, model=Category, category_name=category_name))

        existing_game.game_publisher = []
        if game.get("publishers"):
            for publisher in game.get("publishers"):
                publisher_name = publisher.get("name")
                existing_game.game_publisher.append(self.get_or_create(session=self.session, model=Publisher, publisher_name=publisher_name))

        existing_game.game_ganre = []
        if game.get("genres"):
            for genre in game.get("genres"):
                ganres_name = genre.get("description")
                existing_game.game_ganre.append(self.get_or_create(session=self.session, model=Ganres, ganres_name=ganres_name))

        self.session.commit()  # Підтверджуємо зміни в базі

    def add_new_game(self,game,steam_appid):
        new_game = Game(
            steam_appid=steam_appid,
            name=game.get("name"),
            is_free=game.get("is_free"),
            short_description=game.get("short_description"),
            requirements=game.get("steam_requirements"),
            initial_price=game.get("price_overview", {}).get("initial", 0),
            final_price=game.get("price_overview", {}).get("final", 0),
            final_formatted_price=game.get("price_overview", {}).get("final_formatted", "Free"),
            discount=game.get("price_overview", {}).get("discount_percent", 0),
            metacritic=game.get("metacritic", {}).get("score", -1),
            achievements=game.get("achievements", {}).get("highlighted", {}),
            recomendations=int(game.get("recommendations", {}).get("total", 0)),
            img_url=game.get("capsule_image"),
        )

        # Додаємо категорії, жанри та видавців
        if game.get("categories"):
            for category in game.get("categories"):
                category_name = category.get("description")
                new_game.game_categories.append(
                    self.get_or_create(session=self.session, model=Category, category_name=category_name))

        if game.get("publishers"):
            for publisher in game.get("publishers"):
                publisher_name = publisher.get("name")
                new_game.game_publisher.append(
                    self.get_or_create(session=self.session, model=Publisher, publisher_name=publisher_name))

        if game.get("genres"):
            for genre in game.get("genres"):
                ganres_name = genre.get("description")
                new_game.game_ganre.append(
                    self.get_or_create(session=self.session, model=Ganres, ganres_name=ganres_name))

        self.session.add(new_game)
        self.session.commit()

    def create_gamesdetails_model(self, game_list):
        if not isinstance(game_list, list):
            raise ValueError("Game list must be a list")

        for game in game_list:
            steam_appid = game.get("steam_appid")
            existing_game = self.session.query(Game).filter_by(steam_appid=steam_appid).first()

            if existing_game:
                self.update_game_details(game, existing_game)
            else:
                self.add_new_game(game,steam_appid)



    def parse(self,game_list_appid):
        new_list = []
        for i in game_list_appid:
            result = self.steam.apps.get_app_details(int(i), filters=self.filters)

            if result.get(f"{i}").get("success") == False:
                continue

            new_list.append(result[f'{i}']['data'])
            time.sleep(2)

        self.create_gamesdetails_model(new_list)
