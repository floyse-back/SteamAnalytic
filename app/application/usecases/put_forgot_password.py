from app.domain.users.repository import IUserRepository


class PutForgotPasswordUseCase:
    def __init__(self,user_repository:IUserRepository):
        self.user_repository = user_repository

    async def execute(self,session,user_model,new_password):
        return await self.user_repository.user_password_update(session=session,new_password=new_password,user_model=user_model)
