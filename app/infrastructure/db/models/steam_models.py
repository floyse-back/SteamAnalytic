from datetime import date
from typing import Union

import sqlalchemy
from sqlalchemy import Column, Integer, String, JSON, Date, Boolean, UniqueConstraint, ForeignKey, Index
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.infrastructure.db.database import Base


class SteamEventBase(Base):
    __tablename__ = "steam_events"

    id:Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(String,unique=True)
    type_name:Mapped[str] = mapped_column(String,default="festival")
    date_start:Mapped[date] = mapped_column(Date)
    date_end:Mapped[date] = mapped_column(Date)

class BlockedGames(Base):
    __tablename__ = "blocked_games"
    appid:Mapped[int] = mapped_column(Integer, primary_key=True,nullable=False)

class SafeGames(Base):
    __tablename__ = "safe_games"
    appid:Mapped[int] = mapped_column(Integer, primary_key=True,nullable=False)

class SteamBase(Base):
    __tablename__ = "steambase"

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    appid = Column(String,index=True,unique=True)
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
    ccu = Column(Integer,nullable=True,default=0)

class SteamBaseTemp(Base):
    __tablename__ = "steambase_temp"

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    appid = Column(String,index=True,unique=True)
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
    ccu = Column(Integer,nullable=True,default=0)

class SteamReserveBase(Base):
    __tablename__ = "steambase_copy"

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    appid = Column(String,index=True,unique=True)
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
    ccu = Column(Integer,nullable=True,default=0)


class Game(Base):
    __tablename__ = 'gamesdetails'

    steam_appid = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String,index=True)
    is_free = Column(Boolean)
    short_description = Column(String)
    requirements = Column(JSON)
    initial_price = Column(Integer)
    final_price = Column(Integer)
    final_formatted_price = Column(String)
    metacritic = Column(String)
    discount = Column(Integer)
    achievements = Column(JSON)
    recomendations = Column(Integer)
    img_url = Column(String)
    trailer_url = Column(String,default=None,nullable=True)
    release_data = Column(Date,default= sqlalchemy.func.current_date())
    last_updated = Column(Date,default = sqlalchemy.func.current_date())

    __table_args__ = (
        UniqueConstraint('steam_appid', name='uq_gamesdetails_steam_appid'),
        Index(
            'idx_game_name_trgm',
            'name',
            postgresql_using='gin',
            postgresql_ops={'name': 'gin_trgm_ops'}
        )
    )

    game_ganre = relationship(
        "Ganres",
        secondary="ganre_to_many",
        back_populates="ganre_games",
        lazy="joined"
    )

    game_publisher = relationship(
        "Publisher",
        secondary="publisher_to_many",
        back_populates="publisher_games",
        lazy="joined"
    )

    game_categories = relationship(
        "Category",
        secondary="category_to_many",
        back_populates="category_games",
        lazy="joined"
    )


class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String,unique=True)

    category_games = relationship(
        "Game",
        secondary="category_to_many",
        back_populates = "game_categories"
    )


class Ganres(Base):
    __tablename__ = 'ganres'
    ganres_id = Column(Integer, primary_key=True, index=True)
    ganres_name = Column(String,unique=True)

    ganre_games = relationship(
        "Game",
        secondary="ganre_to_many",
        back_populates="game_ganre"
    )


class Publisher(Base):
    __tablename__ = 'publishers'
    publisher_id = Column(Integer, primary_key=True, index=True)
    publisher_name = Column(String,unique=True)

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


class CategoryToMany(Base):
    __tablename__ = 'category_to_many'

    game_id = Column(ForeignKey("gamesdetails.steam_appid", ondelete="CASCADE"), primary_key = True)
    category_id = Column(ForeignKey("categories.category_id", ondelete="CASCADE"), primary_key = True)
