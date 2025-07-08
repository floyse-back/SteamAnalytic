from app.domain.celery_sender import ICelerySender
from app.infrastructure.celery_app.tasks.steam_tasks import send_email



class CelerySender(ICelerySender):
    async def send_email(self,receiver,token,type):
        send_email.delay(receiver,token,type)