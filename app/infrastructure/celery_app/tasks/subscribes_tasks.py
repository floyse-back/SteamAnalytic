from app.application.services.subsctibes_service.subscribes_service import SubscribesService
from app.utils.dependencies import get_subscribes_service
from app.infrastructure.celery_app.celery_app import app, logger
from ..database import get_db
from ...messages.producer import EventProducer


@app.task
def subscribes_task(sub_type:str)->None:
    subscribes_service:SubscribesService = get_subscribes_service()
    with next(get_db()) as session:
        data = subscribes_service.dispathcher(sub_type,session)
    if data is None:
        logger.error("[x] No subscribe data")
        return None
    event_producer = EventProducer(
        logger = logger
    )
    data = {
        "sub_type":sub_type,
        "body":data
    }
    logger.info("Start Sending Subscribes queue")
    event_producer.send_message(body=data,queue="subscribe_queue")

@app.task
def update_wishlist_batches(data)->None:
    subscribes_service:SubscribesService = get_subscribes_service()
    session = next(get_db())
    logger.info("Update Wishlist Batches queue")
    new_data = subscribes_service.update_game_wishlist(session,data)
    logger.debug("Updated Wishlist Batches queue %s",new_data)
    event_producer = EventProducer(
        logger=logger
    )
    body = {
        "type":"send_and_update_wishlist_games",
        "status": True,
        "data":new_data
    }
    event_producer.send_message(body=body,queue="update_wishlist_batches")