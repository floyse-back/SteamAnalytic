from app.application.dto.steam_dto import GameFullModel, transform_to_dto
from app.domain.steam.sync_repository import INewsRepository


class GetGameFromCategoriesNameUseCase():
    def __init__(self,news_repository:INewsRepository):
        self.news_repository = news_repository

    def execute(self,category:str,session)->dict:
        data = self.news_repository.get_game_from_categorie_name(session=session,category_name=category)
        if data is None:
            return None

        serialize_data = transform_to_dto(GameFullModel,data)

        return serialize_data