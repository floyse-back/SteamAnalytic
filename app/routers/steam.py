from fastapi import APIRouter,Query,Path
from sqlalchemy.ext.asyncio import async_sessionmaker
from ..database.crud import CRUD
from ..database.database import engine
from steam_web_api import Steam
from ..config import STEAM_API_KEY
import asyncio
router = APIRouter()

session = async_sessionmaker(bind=engine,expire_on_commit=False)
steam = Steam(STEAM_API_KEY)
db = CRUD()

@router.get("/get_top_games")
async def get_top_games():
    return {"message": "Top Games"}

@router.get("/best_sallers/")
async def best_sallers(page:int=Query(default=1,gt=0),limit:int=Query(default=100,gt=-1)):
    result = await db.get_most_discount_games(session,page,limit)
    return result

@router.get("/users_full_stats/{user_id}")
async def user_stats(user_id:str):
    try:
        my_int = int(user_id)
        user_data =steam.users.get_user_details(f"{my_int}")
    except Exception as ex:
        user_data = steam.users.search_user(f"{user_id}")
        user_id = user_data["player"]["steamid"]

    user_friends_list = steam.users.get_user_friends_list(f"{user_id}")
    print(user_friends_list)
    user_badges = steam.users.get_user_badges(f"{user_id}")
    print(user_badges)
    user_games = steam.users.get_owned_games(f"{user_id}")
    print(user_games)
    #user_whish_list = steam.users.get_profile_wishlist(f"{user_id}")

    data_dict = {
        "user_data":user_data,
        "user_friends_list":user_friends_list,
        "user_badges":user_badges,
        "user_games":user_games,
    }
    return data_dict

@router.get("/game_stats/{steam_id}")
async def game_stats(steam_id:int =Path(gt=-1)):
    result = steam.apps.get_app_details(steam_id)
    return {"message": f"Game Stats {result}"}

@router.get("/upcoming_release")
async def upcoming_release():
    return {"message": "Upcoming Release"}

@router.get("/api/most_played_games/")
async def most_played_games(limit:int=Query(default=100,gt=-1),page:int=Query(default=1,gt=0)):
    result = await db.get_most_played_page(session,page,limit)

    return result