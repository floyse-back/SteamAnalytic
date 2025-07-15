from app.domain.logger import ILogger
from app.domain.steam.sync_repository import INewsRepository


class SummaryStatisticsSteamUseCase:
    def __init__(self,news_repository:INewsRepository,logger:ILogger):
        self.news_repository = news_repository
        self.logger = logger

    def execute(self,session):
        data = self.news_repository.summary_statistics_steam(session=session)
        self.logger.info("SummaryStatisticsSteamUseCase Get Summary Statistics: %s",data)
        #Serialize Data
        return data