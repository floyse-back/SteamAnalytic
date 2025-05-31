from app.infrastructure.celery_app.celery_app import app

from datetime import date

from app.infrastructure.celery_app.database import get_db
from app.infrastructure.db.models.steam_models import SteamBase, Game
from app.infrastructure.db.models.users_models import RefreshToken
from app.infrastructure.celery_app.utils.steam_parser import SteamParser
from app.infrastructure.celery_app.utils.steam_details_parser import SteamDetailsParser
from sqlalchemy import text,cast,Integer,select,delete,update

from app.infrastructure.email_sender.new_email_sender import EmailSender
from app.infrastructure.logger.logger import logger


@app.task(
    max_retries=2,
    default_retry_delay=100
)
def update_steam_games():
    logger.info("Starting task update_steam_games!")
    session = next(get_db())

    parser = SteamParser()
    generator_data = parser.page_parse()

    session.query(SteamBase).delete()

    for data in generator_data:
        if data != "Server don`t respond":
            session.bulk_save_objects(data)
            session.flush()

    session.commit()
    session.close()
    logger.info("Finished task update_steam_games!")


@app.task(
    max_retries=2,
    default_retry_delay=5
)
def get_game_details():
    logger.info("Starting task get_game_details!")
    session = next(get_db())

    try:
        statement = select(SteamBase.appid).join(Game, cast(SteamBase.appid, Integer) == cast(Game.steam_appid, Integer), isouter=True).filter(Game.steam_appid.is_(None)).order_by(SteamBase.positive.desc()).limit(100)
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


@app.task(
    max_retries=2,
    default_retry_delay=5
)
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
    delete_tokens = delete(RefreshToken).where(RefreshToken.delete_time > date.today())

    session.execute(delete_tokens)
    session.commit()
    logger.info("Finished task delete_refresh_tokens_by_time!")

@app.task
def update_game_icon_url():
    logger.info("Starting task update_game_icon_url!")

    session = next(get_db())
    get_appid_icon_statement = select(SteamBase.appid,Game.img_url).join(Game,cast(SteamBase.appid,Integer) == cast(Game.steam_appid,Integer),isouter=True).where(SteamBase.img_url.is_(None))
    result = session.execute(get_appid_icon_statement).fetchall()

    for element in result:
        stmt = update(SteamBase).where(SteamBase.appid == element[0]).values(img_url=element[1])
        session.execute(stmt)
    session.commit()
    logger.info("Finished task update_game_icon_url!")

@app.task
def update_gamesdetails_from_discount():
    logger.info("Starting task update_gamesdetails_from_discount!")

    session = next(get_db())
    try:
        statement = select(SteamBase.appid).join(Game, cast(SteamBase.appid, Integer) == cast(Game.steam_appid, Integer), isouter=True).filter(Game.steam_appid.is_(None)).order_by(SteamBase.discount.desc())
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

    logger.info("Finished task update_gamesdetails_from_discount!")

@app.task(
    max_retries=3,
    default_retry_delay=2,
    retry_backoff_max = 20
)
def send_email(receiver,url,type):
    logger.info("Starting task send_email %s %s!",receiver,type)
    email_sender = EmailSender()
    email_sender.send_email(receiver,url,type)
    logger.info("Finished task send_email!")