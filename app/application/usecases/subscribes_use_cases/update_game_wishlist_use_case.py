from typing import List

from app.application.dto.steam_dto import GameWishlistModel
from app.domain.logger import ILogger
from app.domain.steam.sync_repository import IGameWishlistRepository


class UpdateGameWishlistUseCase:
    def __init__(self, wishlist_repository:IGameWishlistRepository,logger:ILogger):
        self.wishlist_repository = wishlist_repository
        self.logger = logger

    def execute(self,session,data:List[dict]):
        self.logger.info("UpdateGameWishlistUseCase EXECUTE ")
        self.logger.debug("UpdateGameWishlistUseCase EXECUTE %s",data)
        correct_data = self.wishlist_repository.get_changed_games(appids=data,session=session)
        self.logger.info("Correct Data Steam_Analytic %s",correct_data)
        serialize_data = []
        for game in data:
            for game_correct_data in correct_data:
                if game_correct_data.steam_appid == game['steam_appid'] and (game['price_overview']['final'] != game_correct_data.final_price or game['price_overview']['discount_percent'] != game_correct_data.discount):
                    model = GameWishlistModel(
                            game_id=game_correct_data.steam_appid,
                            name=game_correct_data.name,
                            short_desc=game_correct_data.short_description,
                            price=game_correct_data.final_price,
                            discount=game_correct_data.discount
                        ).model_dump()
                    serialize_data.append(model)
        return serialize_data