from datetime import date
from typing import List, Optional

from app.application.dto.steam_dto import transform_to_dto, GameFullModel
from app.domain.logger import ILogger
from app.domain.steam.sync_repository import INewsRepository


class EventHistorySteamFactsUseCase:
    def __init__(self,news_repository:INewsRepository,logger:ILogger):
        self.news_repository = news_repository
        self.logger = logger

    def execute(self,session)->Optional[List[dict]]:
        self.logger.debug("Start EventHistorySteamFactsUseCase")
        now_date_list = self.__now_date_list()
        data = self.news_repository.event_history_steam_facts(session=session,now_date_list=now_date_list)
        self.logger.debug("Get data from EventHistorySteamFactsUseCase")
        #Серіалізація даних
        if data is None:
            self.logger.info("EventHistorySteamFactsUseCase don`t found facts")
            return None
        self.logger.info("EventHistorySteamFactsUseCase found  %s facts",len(data))
        serialize_data = [transform_to_dto(GameFullModel, i) for i in data]
        self.logger.debug("EventHistorySteamFactsUseCase Serialize data")
        return serialize_data

    def __now_date_list(self)->List[date]:
        date_now = date.today()
        day = date_now.day
        month = date_now.month
        list_date_this_day = []
        this_year = date_now.year-1
        for i in range(this_year,2006,-1):
            try:
                list_date_this_day.append(date(year=i,month=month,day=day))
            except Exception as e:
                continue
        return list_date_this_day