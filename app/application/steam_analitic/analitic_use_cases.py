from sqlalchemy.ext.asyncio import AsyncSession

from .games_for_you import GamesForYou
from .user_rating import UserRating

class AnaliticService:
    def __init__(self):
        self.user_rating = UserRating()
        self.games_for_you = GamesForYou()

    async def analitic_user_rating(self,data:dict):
        return await self.user_rating.create_user_rating(data=data)

    async def analitic_games_for_you(self,data:dict,session:AsyncSession):
        return await self.games_for_you.find_games_for_you(data=data,session = session)