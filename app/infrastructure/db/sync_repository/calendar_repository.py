from datetime import date, timedelta
from typing import List, Tuple, Optional

from sqlalchemy import select, and_, or_

from app.domain.steam.sync_repository import ICalendarSteamEventRepository
from app.infrastructure.db.models.steam_models import SteamEventBase


class CalendarSteamEventRepository(ICalendarSteamEventRepository):
    def update_calendar_data(self,session,data:List[Tuple[str,date,date,str]]):
        unique_events = {}
        for event in data:
            unique_events[event[0]] = event

        for event in unique_events.values():
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

    def get_now_events(self,session,datenow:date=date.today())->Optional[List[SteamEventBase]]:
        next_day = date.today() + timedelta(days=1)
        statement = select(SteamEventBase).filter(or_(
                SteamEventBase.date_start == datenow,
                SteamEventBase.date_end == datenow,
                SteamEventBase.date_start == next_day
            )
        )
        result = session.execute(statement)
        return result.scalars().all()
