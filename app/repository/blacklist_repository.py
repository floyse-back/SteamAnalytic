from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.domain.users.models import RefreshToken, BlackList


class BlackListRepository:
    @staticmethod
    async def add_blacklist_tokens(refresh_tokens:List[RefreshToken],session:AsyncSession):
        for refresh_token in refresh_tokens:
            token_model = BlackList(user_id=refresh_token.user_id,
                                    token=refresh_token.refresh_token,
                                    expires_at=refresh_token.delete_time,
                                    reason= "Token blacklisted"
                                    )
            session.add(token_model)


    @staticmethod
    async def verify_blacklist_token(session:AsyncSession,token:str):
        result = await session.execute(select(BlackList).filter(BlackList.token == token))
        if result.scalars().first():
            return True
        else:
            return False