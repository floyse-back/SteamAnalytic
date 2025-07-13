from datetime import date

from app.application.dto.steam_dto import transform_to_dto, CalendarEventModel
from app.domain.steam.sync_repository import ICalendarSteamEventRepository
from app.infrastructure.logger.logger import logger


class GetCalendarEventNowUseCase:
    def __init__(self, calendar_repository:ICalendarSteamEventRepository):
        self.calendar_repository = calendar_repository

    def execute(self,session):
        data = self.calendar_repository.get_now_events(session=session,datenow = date.today())
        logger.info(f"Data Type Calendar Now: {type(data)}")
        logger.error(f"Data Type Calendar Now: %s",data)
        if data is None:
            return None

        #Seriailze and Dump
        serialize_data = [transform_to_dto(CalendarEventModel,i) for i in data]
        logger.info(f"Data Type Calendar Now: {serialize_data}")
        return serialize_data