from fastapi import APIRouter,Depends, HTTPException

from steam_web_api import Steam
from app.utils.config import STEAM_API_KEY,HOST
from httpx import AsyncClient

from app.infrastructure.db.database import get_async_db
from app.utils.dependencies import user_auth_check
from app.application.steam_analitic.analitic_use_cases import AnaliticService

router = APIRouter(prefix="/api/v1/analytics")

steam = Steam(STEAM_API_KEY)
analitic_service = AnaliticService()


@router.get("/user_battle",response_model=None)
async def analytics(user1_id:str, user2_id:str, auth = Depends(user_auth_check)):
    if user1_id == user2_id:
        raise HTTPException(status_code=404)
    async with AsyncClient(base_url=f"http://{HOST}") as client:
        user_1 = await client.request("GET",f"/api/v1/steam/users_full_stats/{user1_id}",params={"friends_details":"false"})
        user_2 = await client.request("GET", f"/api/v1/steam/users_full_stats/{user2_id}",params={"friends_details":"false"})

    return {f"{user1_id}": user_1.json(),
            f"{user2_id}": user_2.json()
            }

@router.get("/user_score/")
async def user_score_generate(user:str, auth = Depends(user_auth_check)):
    async with AsyncClient(base_url=f"http://{HOST}") as client:
        user_data = await client.request("GET",f"api/v1/steam/users_full_stats/{user}",params={"friends_details":"false"})

    result = await analitic_service.analitic_user_rating(user_data.json())
    return {
        "user_rating": result
    }

@router.get("/friends_list/")
async def friend_game_list(user_id: int=None, auth = Depends(user_auth_check)):
    response= steam.users.get_user_friends_list(f"{user_id}")
    return response

@router.get("/games_for_you")
async def games_for_you(user:str,session = Depends(get_async_db), auth = Depends(user_auth_check)):
    async with AsyncClient(base_url=f"http://{HOST}") as client:
        user_1 = await client.request("GET",f"/api/v1/steam/user_games_played",params={"user":f"{user}"})

    if user_1.status_code != 200:
        raise HTTPException(status_code=401)

    result = await analitic_service.analitic_games_for_you(user_1.json(),session = session)
    return result

@router.get("/salling_for_you")
async def salling_for_games_you(user:str,auth = Depends(user_auth_check),session = Depends(get_async_db)):
    async with AsyncClient(base_url=f"http://{HOST}") as client:
        user_1 = await client.request("GET",f"/api/v1/steam/user_games_played",params={"user":f"{user}"})

    if user_1.status_code != 200:
        raise HTTPException(status_code=401)

    result = await analitic_service.salling_for_you_games(user_1.json(),session=session)
    return result

@router.get("/user_achivements/")
async def user_achivements(steam_id:int, app_id:int, auth = Depends(user_auth_check)):
    response = steam.apps.get_user_achievements(steam_id,app_id)

    return response


