from pydantic import BaseModel

from app.application.services.news_service.news_service import NewsService
from app.infrastructure.celery_app.celery_app import app, logger
from app.infrastructure.celery_app.database import get_db

from app.infrastructure.messages.producer import EventProducer
from app.utils.dependencies import get_news_service

@app.task
def update_steam_events():
    logger.info(f"Updating Steam Events")
    news_service:NewsService = get_news_service()
    session= next(get_db())
    news_service.update_calendar_events(session=session)
    logger.info(f"Steam Events Updated")

@app.task
def news_task_creator(type_news:str):
    logger.info("type_news")
    session = next(get_db())
    news_service: NewsService = get_news_service()
    data = news_service.dispathcher(func_name=f"{type_news}",session=session)
    if data is None:
        logger.info("Don`t Finded games from {}".format(type_news))
        return None

    event_producer = EventProducer(
        logger=logger,
    )
    if data and isinstance(data[-1],BaseModel):
        data = [i.model_dump() for i in data]
    logger.info(f"Data:%s\nType%s",data,type(data))
    body = {
        "type_news":f"{type_news}",
        "data":data
    }
    if data:
        event_producer.send_message(body=body,queue="news_queue")

    logger.debug("news_new_release data: {}".format(data))

@app.task
def news_game_from_type(name:str,type:str="ganre"):
    """
    Важливо ganre_name має бути українською мовою
    """
    logger.info("NewsGameFromGanre: Execute %s",name)
    session = next(get_db())
    news_service: NewsService = get_news_service()
    if type == "ganre":
        data = news_service.game_from_ganre(ganre_name=name,session=session)
        type_news = "news_game_from_ganre"
    else:
        data = news_service.game_from_categories(categories=name,session=session)
        type_news = "news_game_from_categories"


    if data is None:
        logger.info("Don`t Finded games from {}".format(name))
        return None

    event_producer = EventProducer(logger=logger)
    body = {
        "type_news":f"{type_news}{name}",
        "data":data if isinstance(data,list) else [data]
    }
    event_producer.send_message(body=body,queue="news_queue")


