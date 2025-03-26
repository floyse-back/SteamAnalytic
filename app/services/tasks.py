from .celery_app import app

from datetime import date

from .database import get_db
from ..database.models import SteamBase, Game, TokenBase
from .utils.steam_parser import SteamParser
from .utils.steam_details_parser import SteamDetailsParser
from sqlalchemy import text,cast,Integer,select,delete

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
        statement = select(SteamBase.appid).join(Game, cast(SteamBase.appid, Integer) == cast(Game.steam_appid, Integer), isouter=True).filter(Game.steam_appid.is_(None)).order_by(SteamBase.positive).limit(10)
        result = session.execute(statement)
        result = result.scalars().all()
        parser = SteamDetailsParser(session=session)

        logger.info(f"Get games")
        parser.parse(game_list_appid=result)

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    logger.info("Finished task get_game_details!")


@app.task
def update_or_add_game(game,steam_id):
    logger.info("Starting task update_or_add_game!")
    session = next(get_db())

    if game.get(f"{steam_id}").get("success")==False:
        return logger.info(f"Game not found")
    game = game.get(f"{steam_id}").get("data")

    steamparser=SteamDetailsParser(session=session)
    steamparser.create_gamesdetails_model([game])

    logger.info(f"Game update or add {steam_id}")

@app.task
def delete_refresh_tokens_by_time():
    logger.info("Starting task delete_refresh_tokens_by_time!")
    session = next(get_db())
    delete_tokens = delete(TokenBase).where(TokenBase.delete_time > date.today())

    session.execute(delete_tokens)
    session.commit()
    logger.info("Finished task delete_refresh_tokens_by_time!")
