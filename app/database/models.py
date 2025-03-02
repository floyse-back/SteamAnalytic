from sqlalchemy import Column, Boolean, Integer, String, JSON, Date, ForeignKey,UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
import sqlalchemy
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
    __tablename__ = "historysteambase"

    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    data = Column(JSONB,nullable=False)
    snapshot_date = Column(Date,nullable=False,default=sqlalchemy.func.current_date())

class Game(Base):
    __tablename__ = 'gamesdetails'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    steam_appid = Column(Integer, nullable=False,unique=True)
    publisher = Column(String)
    developer = Column(String)
    is_free = Column(Boolean)
    short_description = Column(String)
    requirements = Column(JSONB)
    initial_price = Column(Integer)
    final_price = Column(Integer)
    metacritic = Column(String)
    discount = Column(Integer)
    release_date = Column(Date)
    categories = Column(JSONB)
    ganres = Column(JSONB)
    achievements = Column(JSONB)
    release_data = Column(JSONB)
    recomendations = Column(Integer)

    __table_args__ = (
        UniqueConstraint('steam_appid', name='uq_gamesdetails_steam_appid'),
    )

    game_ganre = relationship(
        "Ganres",
        secondary="ganre_to_many",
        back_populates="ganre_games"
    )

    game_publisher = relationship(
        "Publisher",
        secondary="publisher_to_many",
        back_populates="publisher_games"
    )

class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)

class Ganres(Base):
    __tablename__ = 'ganres'
    ganres_id = Column(Integer, primary_key=True, index=True)
    ganres_name = Column(String)

    ganre_games = relationship(
        "Game",
        secondary="ganre_to_many",
        back_populates="game_ganre"
    )

class Publisher(Base):
    __tablename__ = 'publishers'
    publisher_id = Column(Integer, primary_key=True, index=True)
    publisher_name = Column(String)

    publisher_games = relationship(
        "Game",
        secondary="publisher_to_many",
        back_populates="game_publisher"
    )

class GanreToMany(Base):
    __tablename__ = 'ganre_to_many'

    game_id = Column(ForeignKey("gamesdetails.steam_appid", ondelete="CASCADE"), primary_key=True)
    ganre_id = Column(ForeignKey("ganres.ganres_id", ondelete="CASCADE"), primary_key=True)

class PublisherToMany(Base):
    __tablename__ = 'publisher_to_many'

    game_id = Column(ForeignKey("gamesdetails.steam_appid", ondelete="CASCADE"), primary_key=True)
    publisher_id = Column(ForeignKey("publishers.publisher_id", ondelete="CASCADE"), primary_key=True)