from datetime import date
from typing import List

from app.domain.steam.sync_repository import INewsRepository


class EventHistorySteamFactsUseCase:
    def __init__(self,news_repository:INewsRepository):
        self.news_repository = news_repository

    def execute(self,session):
        now_date_list = self.__now_date_list()
        return self.news_repository.event_history_steam_facts(session=session,now_date_list=now_date_list)

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