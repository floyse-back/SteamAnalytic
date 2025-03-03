from .celery_app import app

from .database import get_db
from ..database.models import SteamBase,Game,Publisher,Ganres,Category
from .utils.steam_parser import SteamParser
from .utils.steam_details_parser import SteamDetailsParser
from sqlalchemy import text,cast,Integer,select,insert

import logging

logger = logging.getLogger(__name__)

@app.task
def update_steam_games():
    logger.info("Starting task update_steam_games!")
    session = next(get_db())

    parser = SteamParser()
    generator_data = parser.page_parse()

    session.execute(text("""
        INSERT INTO historysteambase (data)
        SELECT to_jsonb(array_agg(steambase.*))
        FROM steambase;
        """))
    session.query(SteamBase).delete()

    for data in generator_data:
        if data != "Server don`t respond":
            session.bulk_save_objects(data)
            session.flush()

    session.commit()
    session.close()
    return "Finished task update_steam_games!"


@app.task
def get_game_details():
    logger.info("Starting task get_game_details!")
    session = next(get_db())

    try:
        statement = select(SteamBase.appid).join(Game, cast(SteamBase.appid, Integer) == cast(Game.steam_appid, Integer), isouter=True).filter(Game.steam_appid.is_(None)).order_by(SteamBase.positive).limit(100)
        result = session.execute(statement)
        result = result.scalars().all()
        parser = SteamDetailsParser(result,session=session)

        logger.info(f"Get games")
        games = parser.parse()

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    logger.info("Finished task get_game_details!")
