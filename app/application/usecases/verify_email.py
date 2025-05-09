




class VerifyEmailUseCase:
    def __init__(self,user_repository):
        self.user_repository = user_repository

    async def execute(self,session,user_model,status=True):
        await self.user_repository.user_verify_update(session=session,status=True,user_model=user_model)
        return {"Email Verified": True}