from app.application.services.news_service.news_service import NewsService
from app.infrastructure.celery_app.celery_app import app
from app.infrastructure.celery_app.database import get_db
from app.infrastructure.logger.logger import logger
from app.infrastructure.messages.producer import EventProducer
from app.utils.dependencies import get_news_service

@app.task
def news_new_release(type_news:str):
    logger.info("news_new_release")
    session = next(get_db())
    news_service: NewsService = get_news_service()
    data = news_service.dispathcher(func_name=f"{type_news}",session=session)
    event_producer = EventProducer()
    body = {
        "type":f"{type_news}",
        "data":data
    }
    if data:
        event_producer.send_message(body=body,queue="news_queue")

    logger.debug("news_new_release data: {}".format(data))

