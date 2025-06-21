from fastapi import APIRouter, Query, Depends

from steam_web_api import Steam
from app.utils.config import STEAM_API_KEY
from app.infrastructure.celery_app.steam_tasks import update_or_add_game
from app.utils.dependencies import get_steam_service,get_async_db

from typing import List, Optional

router = APIRouter()

steam = Steam(STEAM_API_KEY)



@router.get("/best_sallers/")
async def best_sallers(session = Depends(get_async_db),steam_service = Depends(get_steam_service),page:int=Query(default=1,gt=0),limit:int=Query(default=100,gt=-1)):
    return await steam_service.best_sallers(session,page,limit)

@router.get("/users_full_stats/{user}")
async def user_full_stats(user:str,user_badges:bool = Query(default=True),steam_service = Depends(get_steam_service),friends_details:bool = Query(default=True),user_games:bool = Query(default=True)):
    return await steam_service.user_full_stats(user,user_badges,friends_details,user_games)

@router.get("/game_stats/{steam_id}")
async def game_stats(steam_id:int,steam_service = Depends(get_steam_service)):
    result = await steam_service.game_stats(steam_id)
    update_or_add_game.apply_async(args=[result,steam_id])
    return result

@router.get("/get_top_games/")
async def get_top_games(session=Depends(get_async_db),steam_service = Depends(get_steam_service),limit:int=Query(default=100,gt=-1),page:int=Query(default=1,gt=0)):
    return await steam_service.get_top_games(session,limit,page)

@router.get("/game_achivements")
async def game_achivements(game_id,steam_service = Depends(get_steam_service)):
    return await steam_service.game_achivements(game_id)

@router.get("/user_games_played")
async def user_games_play(user:str,steam_service = Depends(get_steam_service)):
    return await steam_service.user_games_play(user)

@router.get("/search_game/")
async def search_game(steam_service = Depends(get_steam_service),name:Optional[str] = Query(default=None),to_price: Optional[int] = Query(default=None),out_price:Optional[int] = Query(default=None),category: Optional[List] = Query(default=None),ganre:Optional[List] = Query(default=None),discount:Optional[int] = Query(default=None),publisher:Optional[List] = Query(default=None),session = Depends(get_async_db)):
    return await steam_service.search_game(session=session,name=name,category=category,discount=discount,publisher=publisher,ganre=ganre,to_price=to_price,out_price=out_price)