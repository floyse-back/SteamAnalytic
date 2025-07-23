from app.domain.celery_sender import ICelerySender



class CelerySender(ICelerySender):
    async def send_email(self,receiver,token,type):
        from app.infrastructure.celery_app.tasks.steam_tasks import send_email
        send_email.delay(receiver,token,type)