from app.domain.logger import ILogger
from app.infrastructure.db.models.users_models import UserModel


class VerifyEmailUseCase:
    def __init__(self,user_repository,logger:ILogger):
        self.user_repository = user_repository
        self.logger = logger

    async def execute(self,session,user_model:UserModel,status=True):
        await self.user_repository.user_verify_update(session=session,status=True,user_model=user_model)
        return {"Email Verified": True}