from typing import List

from app.domain.steam.sync_repository import ISafegameRepository, IBlockedGamesRepository
from app.infrastructure.db.sync_repository.BlockedGamesRepository import BlockedGamesRepository


class CheckGameBaseUseCase:
    def __init__(self,blocked_repository:IBlockedGamesRepository,safe_games_repository:ISafegameRepository):
        self.blocked_repository = blocked_repository
        self.safe_games_repository = safe_games_repository

    def execute(self,appids:List[int],session):
        """
        Повертає список dict з ключами success:True (Якщо гра безпечна), success:False
        Якщо гру треба перевірити якщо гра не безпечна ми її не повертаємо
        """
        safe_games_list = self.safe_games_repository.get_safe_games_from_appids(appids,session)
        blocked_games_list = self.blocked_repository.get_blocked_games_from_appids(appids,session)

        answer_data = []
        for i in blocked_games_list:
            appids.remove(i.appid)
        for i in safe_games_list:
            appid = i.appid
            appids.remove(appid)
            answer_data.append(
                {
                    "appid": appid,
                    "success": True
                }
            )
        for i in appids:
            answer_data.append(
            {
                "appid":i,
                "success":False
                }
            )
        return answer_data