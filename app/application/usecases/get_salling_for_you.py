from app.application.exceptions.exception_handler import GamesNotFound
from app.domain.logger import ILogger
from app.domain.steam.repository import IAnaliticsRepository
from app.domain.steam.usecases.game_for_you import IGameForYou


class GetSallingForYouUseCase(IGameForYou):
    def __init__(self, analitic_repository: IAnaliticsRepository,logger:ILogger):
        super().__init__(analitic_repository,logger=logger)

    async def get_games(self, session, count_dict, appid_list,page:int=1,limit:int=10):
        if count_dict.get("ganres_dict") == [] and count_dict.get("publishers_dict") == [] and count_dict.get(
                "categories_dict") == []:
            raise GamesNotFound()

        data = await self.analitic_repository.salling_for_you(session=session, ganres_data=count_dict.get("ganres_dict"),
                                                            category_data=count_dict.get("categories_dict"),
                                                            steam_appids=appid_list,
                                                            page=page,limit=limit
                                                            )
        return data