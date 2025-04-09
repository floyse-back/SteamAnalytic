from sqlalchemy.ext.asyncio import AsyncSession

from .games_for_you import GamesForYou, SallingForYou
from .user_rating import UserRating

class AnaliticService:
    def __init__(self):
        self.user_rating = UserRating()
        self.games_for_you = GamesForYou()
        self.salling_for_you = SallingForYou()

    async def analitic_user_rating(self,data:dict):
        return await self.user_rating.create_user_rating(data=data)

    async def analitic_games_for_you(self,data:dict,session:AsyncSession):
        return await self.games_for_you.find_games_for_you(data=data,session = session)

    async def analitic_user_battle(self,user1_data:dict,user2_data:dict):
        return {}

    async def salling_for_you_games(self,data:dict,session:AsyncSession):
        return await self.salling_for_you.find_games_for_you(data=data,session=session)
