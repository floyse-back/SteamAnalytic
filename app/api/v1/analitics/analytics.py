from fastapi import APIRouter,Depends, HTTPException,Request

from app.api.v1.analitics.utils.user_rating import UserRating
from app.api.v1.analitics.utils.utils import AnaliticGameForYou
from app.repository.database import get_async_db
from app.repository.refresh_token_repository import RefreshTokenORM
from steam_web_api import Steam
from app.core.config import STEAM_API_KEY,HOST
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
        user_1 = await client.request("GET",f"/api/v1/steam/users_full_stats/{user1_id}",params={"friends_details":"false"})
        user_2 = await client.request("GET", f"/api/v1/steam/users_full_stats/{user2_id}",params={"friends_details":"false"})

    return {f"{user1_id}": user_1.json(),
            f"{user2_id}": user_2.json()
            }

@router.get("/user_score/")
async def user_score_generate(user:str,auth = Depends(user_auth_check)):
    user_rating = UserRating()

    async with AsyncClient(base_url=f"http://{HOST}") as client:
        user_data = await client.request("GET",f"api/v1/steam/users_full_stats/{user}",params={"friends_details":"false"})

    result = await user_rating.create_user(user_data.json())
    return {
        "user_rating": result
    }

@router.get("/friends_list/")
async def friend_game_list(user_id: int=None,auth = Depends(user_auth_check)):
    response= steam.users.get_user_friends_list(f"{user_id}")
    return response

@router.get("/games_for_you")
async def games_for_you(user:str,auth = Depends(user_auth_check)):
    async with AsyncClient(base_url=f"http://{HOST}") as client:
        user_1 = await client.request("GET",f"/api/v1/steam/users_full_stats/{user}")

    if user_1.status_code != 200:
        raise HTTPException(status_code=404)

    game_data = user_1.json()['user_games']['games']
    analitic = AnaliticGameForYou(game_data)

    return {"Hello World":"Stress Test"}

@router.get("/salling_for_you")
async def salling_for_you(auth = Depends(user_auth_check)):
    pass

@router.get("/user_achivements/")
async def user_achivements(steam_id:int,app_id:int,auth = Depends(user_auth_check)):
    response = steam.apps.get_user_achievements(steam_id,app_id)

    return response


