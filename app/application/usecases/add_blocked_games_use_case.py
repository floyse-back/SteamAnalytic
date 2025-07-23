from app.domain.steam.sync_repository import IBlockedGamesRepository


class AddBlockedGamesUseCase:
    def __init__(self,blocked_repository:IBlockedGamesRepository):
        self.blocked_repository = blocked_repository

    def execute(self,appid:int,session):
        return self.blocked_repository.add_blocked_games(appid,session)