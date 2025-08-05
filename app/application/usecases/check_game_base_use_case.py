from typing import List

from app.domain.logger import ILogger
from app.domain.steam.sync_repository import ISafegameRepository, IBlockedGamesRepository


class CheckGameBaseUseCase:
    def __init__(self,blocked_repository:IBlockedGamesRepository,safe_games_repository:ISafegameRepository,logger:ILogger):
        self.blocked_repository = blocked_repository
        self.safe_games_repository = safe_games_repository
        self.logger = logger

    def execute(self,appids:List[str],session):
        """
        Повертає список dict з ключами success:True (Якщо гра безпечна), success:False
        Якщо гру треба перевірити якщо гра не безпечна ми її не повертаємо
        """
        safe_games_list = self.safe_games_repository.get_safe_games_from_appids(appids,session)
        blocked_games_list = self.blocked_repository.get_blocked_games_from_appids(appids,session)

        answer_data = []
        self.logger.info(f"safe_games_list: {safe_games_list}")
        self.logger.info(f"blocked_games_list: {blocked_games_list}")
        for i in blocked_games_list:
            appid = str(i.appid)
            self.logger.debug(f"i: {i}")
            self.logger.debug(f"i: {appids}")
            appids.remove(appid)
        for i in safe_games_list:
            appid = str(i.appid)
            self.logger.info(f"i: {i}")
            self.logger.info(f"i: {appids}")
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