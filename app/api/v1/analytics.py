from fastapi import APIRouter, HTTPException
from steam_web_api import Steam
from app.config import STEAM_API_KEY,HOST
from httpx import AsyncClient
router = APIRouter(prefix="/api/v1/analytics")

steam = Steam(STEAM_API_KEY)


@router.get("/user_battle")
async def analytics(user1_id:str, user2_id:str):
    if user1_id == user2_id:
        raise HTTPException(status_code=404)
    async with AsyncClient(base_url=f"http://{HOST}") as client:
        user_1 = await client.request("GET",f"/api/v1/steam/users_full_stats/{user1_id}")
        user_2 = await client.request("GET", f"/api/v1/steam/users_full_stats/{user2_id}")

    return {f"{user1_id}": user_1.json(),
            f"{user2_id}": user_2.json()
            }

@router.get("/friends_top_games")
async def friends_top_games():
    return {"message": "Hello World"}

@router.get("/popular_games/")
async def popular_games(ganre: str=None):
    return {"message": "popular games"}

@router.get("/friends_activity_track")
async def friends_activity_track():
    return {"message": "friends activity track"}

@router.get("/friends_list/")
async def friend_game_list(user_id: int=None):
    response= steam.users.get_user_friends_list(f"{user_id}")
    return response

