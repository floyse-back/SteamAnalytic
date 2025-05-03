from app.domain.celery_sender import ICelerySender
from app.infrastructure.celery_app.steam_tasks import send_email



class CelerySender(ICelerySender):
    async def send_email(self,receiver,url,type):
        send_email.delay(receiver,url,type)