from app.application.services.subsctibes_service.subscribes_service import SubscribesService
from app.utils.dependencies import get_subscribes_service
from app.infrastructure.celery_app.celery_app import app, logger
from ..database import get_db


@app.task
def subscribes_task(sub_type:str)->None:
    subscribes_service:SubscribesService = get_subscribes_service()
    with next(get_db()) as session:
        subscribes_service.dispathcher(sub_type,session)

@app.task
def update_wishlist_batches(data)->None:
    subscribes_service:SubscribesService = get_subscribes_service()
    with next(get_db()) as session:
        subscribes_service.update_game_wishlist(session,data)