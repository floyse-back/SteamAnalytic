from app.application.exceptions.exception_handler import GamesNotFound
from app.domain.steam.repository import IAnaliticsRepository
from app.domain.usecases.game_for_you import IGameForYou


class GetSallingForYouUseCase(IGameForYou):
    def __init__(self, analitic_repository: IAnaliticsRepository):
        super().__init__(analitic_repository)

    async def get_games(self, session, count_dict, appid_list):
        if count_dict.get("ganres_dict") == [] and count_dict.get("publishers_dict") == [] and count_dict.get(
                "categories_dict") == []:
            raise GamesNotFound()

        data = await self.analitic_repository.salling_for_you(session=session, ganres_data=count_dict.get("ganres_dict"),
                                                            category_data=count_dict.get("categories_dict"),
                                                            steam_appids=appid_list)
        return data