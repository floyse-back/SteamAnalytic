from fastapi import APIRouter,Depends, HTTPException,Request

from app.database.database import get_async_db
from app.database.orm import RefreshTokenORM
from steam_web_api import Steam
from app.config import STEAM_API_KEY,HOST
from httpx import AsyncClient
from app.api.v1.auth.utils import decode_jwt
router = APIRouter(prefix="/api/v1/analytics")

steam = Steam(STEAM_API_KEY)

refresh_token = RefreshTokenORM()

async def user_auth_check(request: Request,session = Depends(get_async_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    decoded_token = decode_jwt(token)
    await refresh_token.verify_refresh_token(session=session,refresh_token=token)


    return decoded_token

@router.get("/user_battle")
async def analytics(user1_id:str, user2_id:str,auth = Depends(user_auth_check)):
    if user1_id == user2_id:
        raise HTTPException(status_code=404)
    async with AsyncClient(base_url=f"http://{HOST}") as client:
        user_1 = await client.request("GET",f"/api/v1/steam/users_full_stats/{user1_id}")
        user_2 = await client.request("GET", f"/api/v1/steam/users_full_stats/{user2_id}")

    return {f"{user1_id}": user_1.json(),
            f"{user2_id}": user_2.json()
            }

@router.get("/friends_top_games")
async def friends_top_games(auth = Depends(user_auth_check)):
    return {"message": "Hello World"}

@router.get("/popular_games/")
async def popular_games(ganre: str=None,auth=Depends(user_auth_check),):
    return {"message": "popular games"}

@router.get("/friends_list/")
async def friend_game_list(user_id: int=None,auth = Depends(user_auth_check)):
    response= steam.users.get_user_friends_list(f"{user_id}")
    return response

@router.get("/games_for_you")
async def games_for_you(auth = Depends(user_auth_check)):
    pass

@router.get("/salling_for_you")
async def salling_for_you(auth = Depends(user_auth_check)):
    pass


