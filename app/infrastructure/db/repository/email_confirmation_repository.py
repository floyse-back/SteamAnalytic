from sqlalchemy import select, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.users.repository import IEmailConfirmationRepository
from app.infrastructure.db.models.users_models import EmailConfirmed, UserModel

import datetime

from app.infrastructure.exceptions.exception_handler import InfrastructureUserRegister, InfrastructureTokenNotFound


class EmailConfirmationRepository(IEmailConfirmationRepository):

    async def create_confirm_token(self,session:AsyncSession,token:str,type:str,user_model:UserModel):
        email_model =EmailConfirmed(
            type=type,
            token=token,
        )

        email_model.user = user_model

        session.add(email_model)
        await session.commit()

    async def verify_confirm_token(self,session:AsyncSession,token:str,type:str):
        statement = select(EmailConfirmed).filter(EmailConfirmed.token == token).filter(EmailConfirmed.type == type).where(EmailConfirmed.expires_at >= datetime.datetime.now())

        result = await session.execute(statement)
        instance = result.scalars().first()

        if not instance:
            raise InfrastructureTokenNotFound
        return instance

    async def delete_confirm_token(self,session,type:str,user_id:int):
        statement = delete(EmailConfirmed).where(or_(EmailConfirmed.type == type,EmailConfirmed.user_id == user_id))

        await session.execute(statement)
        await session.commit()

