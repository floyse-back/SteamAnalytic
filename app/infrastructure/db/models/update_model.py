import datetime

from sqlalchemy import Date, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.database import Base


class UpdateDateModel(Base):
    __tablename__ = "update_steam_base"
    id:Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    update_steam_date:Mapped[datetime.date] = mapped_column(Date, default=func.current_date())