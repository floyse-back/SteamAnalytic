from app.domain.steam.sync_repository import ISafegameRepository


class AddSafeGamesUseCase:
    def __init__(self,safe_game_repository:ISafegameRepository):
        self.safe_game_repository = safe_game_repository

    def execute(self,session,appid:int):
        self.safe_game_repository.add_safe_games(appid=appid,session=session)