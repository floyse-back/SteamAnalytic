from fastapi import APIRouter, Query, Path, HTTPException, Depends
from app.repository.steam_repository import SteamRepository
from app.repository.database import get_async_db
from steam_web_api import Steam
from httpx import AsyncClient
from app.core.config import STEAM_API_KEY
from app.tasks.steam_tasks import update_or_add_game
router = APIRouter(prefix="/api/v1/steam")

steam = Steam(STEAM_API_KEY)
db = SteamRepository()

@router.get("/best_sallers/")
async def best_sallers(session = Depends(get_async_db),page:int=Query(default=1,gt=0),limit:int=Query(default=100,gt=-1)):
    result = await db.get_most_discount_games(session,page,limit)
    return result

@router.get("/users_full_stats/{user}")
async def user_full_stats(user:str,user_badges:bool = Query(default=True),friends_details:bool = Query(default=True),user_games:bool = Query(default=True)):
    try:
        my_int = int(user)
        user_data =steam.users.get_user_details(f"{my_int}")
    except Exception:
        user_data = steam.users.search_user(f"{user}")
        user = user_data["player"]["steamid"]

    try:
        data_dict = dict()
        data_dict["user_data"] = user_data
        data_dict["user_friends_list"] = steam.users.get_user_friends_list(f"{user}",enriched=friends_details)
        data_dict["user_badges"] = steam.users.get_user_badges(f"{user}") if user_badges else None
        data_dict["user_games"] = steam.users.get_owned_games(f"{user}") if user_games else None
    except Exception:
        return HTTPException(
            status_code = 404,
            detail = f"User {user} not found",
            headers = {"WWW-Authenticate": "Bearer"},
        )

    return data_dict

@router.get("/game_stats/{steam_id}")
async def game_stats(steam_id:int =Path(gt=-1)):
    filters ='basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,recommendations,achievements'
    result = steam.apps.get_app_details(steam_id,filters=filters)

    update_or_add_game.apply_async(args=[result,steam_id])
    return result

@router.get("/get_top_games/")
async def get_top_games(session=Depends(get_async_db),limit:int=Query(default=100,gt=-1),page:int=Query(default=1,gt=0)):
    result = await db.get_top_games(session,page,limit)

    return result

@router.get("/game_achivements")
async def game_achivements(game_id):
    async with AsyncClient() as client:
        response = await client.get(f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/?gameid={game_id}")

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")

    return response.json()

@router.get("/user_games_played")
async def user_games_play(user:str):
    try:
        my_int = int(user)
    except Exception:
        user_data = steam.users.search_user(f"{user}")
        print(user_data)
        user = user_data["player"]["steamid"]

    response = steam.users.get_owned_games(f"{user}")

    return response