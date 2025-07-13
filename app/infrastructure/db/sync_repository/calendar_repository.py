from datetime import date
from typing import List, Tuple, Optional

from sqlalchemy import select, and_

from app.domain.steam.sync_repository import ICalendarSteamEventRepository
from app.infrastructure.db.models.steam_models import SteamEventBase


class CalendarSteamEventRepository(ICalendarSteamEventRepository):
    def update_calendar_data(self,session,data:List[Tuple[str,date,date,str]]):
        for event in data:
            statement = select(SteamEventBase).filter(SteamEventBase.name==event[0])
            result = session.execute(statement)
            model = result.scalars().first()

            if model is None:
                model = SteamEventBase(
                    name=event[0],
                    date_start=event[1],
                    date_end=event[2],
                )
                session.add(model)
            else:
                model.name = event[0]
                model.date_start = event[1]
                model.date_end = event[2]

        session.commit()

    def get_calendar_events(self,session)->Optional[List[SteamEventBase]]:
        statement = select(SteamEventBase).order_by(SteamEventBase.date_start)
        result = session.execute(statement)
        return result.scalars().all()

    def get_now_events(self,session,datenow:date)->Optional[List[SteamEventBase]]:
        statement = select(SteamEventBase).filter(and_(
                SteamEventBase.date_start <= datenow,
                SteamEventBase.date_end >= datenow,
            )
        )
        result = session.execute(statement)
        return result.scalars().all()
