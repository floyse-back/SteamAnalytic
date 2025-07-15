from datetime import date

from app.application.dto.steam_dto import transform_to_dto, CalendarEventModel
from app.domain.logger import ILogger
from app.domain.steam.sync_repository import ICalendarSteamEventRepository


class GetCalendarEventNowUseCase:
    def __init__(self, calendar_repository:ICalendarSteamEventRepository,logger:ILogger):
        self.calendar_repository = calendar_repository
        self.logger = logger

    def execute(self,session):
        data = self.calendar_repository.get_now_events(session=session,datenow = date.today())
        self.logger.info(f"GetCalendarEventNowUseCase execute len: %s",len(data))
        self.logger.debug(f"GetCalendarEventNowUseCase execute",data)
        if data is None:
            return None

        #Seriailze and Dump
        serialize_data = [transform_to_dto(CalendarEventModel,i) for i in data]
        self.logger.info(f"Data Type Calendar Now: %s",len(serialize_data))
        return serialize_data