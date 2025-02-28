from sqlalchemy import Column, Integer, String,JSON,Date
from .database import Base

class SteamBase(Base):
    __tablename__ = "steambase"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String)
    appid = Column(String)
    developer = Column(String)
    publisher = Column(String)
    positive = Column(Integer)
    negative = Column(Integer)
    average_forever = Column(Integer)
    average_2weeks =Column(Integer)
    median_forever = Column(Integer)
    median_2weeks = Column(Integer)
    price = Column(Integer)
    discount = Column(Integer)
    img_url = Column(String,nullable=True,default=None)

class HistoricalSteamBase(Base):
    __tablename__ = "historicalsteambase"

    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    data = Column(JSON,nullable=False)
    snapshot_date = Column(Date,nullable=False)
