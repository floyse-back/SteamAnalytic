from app.domain.steam.sync_repository import INewsRepository


class SummaryStatisticsSteamUseCase:
    def __init__(self,news_repository:INewsRepository):
        self.news_repository = news_repository

    def execute(self,session):
        data = self.news_repository.summary_statistics_steam(session=session)

        #Serialize Data
        return data