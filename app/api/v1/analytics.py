from fastapi import APIRouter,Depends,Query
from starlette.responses import JSONResponse

from app.application.dto.steam_dto import SteamRatingModel, UserComparison, FriendsListModel
from app.infrastructure.db.database import get_async_db
from app.utils.dependencies import user_auth_check, get_analitic_service

router = APIRouter(dependencies=[Depends(user_auth_check)])


@router.get("/user_battle",response_model=UserComparison)
async def analytics(user1_id:str, user2_id:str,analitic_service = Depends(get_analitic_service)):
    return await analitic_service.analitic_user_battle(user1_id,user2_id)


@router.get("/user_score",response_model=SteamRatingModel)
async def user_score_generate(user:str,analitic_service = Depends(get_analitic_service)):
    return await analitic_service.analitic_user_rating(user)


@router.get("/friends_list",response_model=FriendsListModel)
async def friend_game_list(user:str,analitic_service = Depends(get_analitic_service)):
    return await analitic_service.friends_game_list(user=user)


@router.get("/games_for_you")
async def games_for_you(user:str,page:int=Query(default=1,gt=0),limit:int=Query(default=100,gt=-1),session = Depends(get_async_db),analitic_service = Depends(get_analitic_service)):
    return await analitic_service.analitic_games_for_you(user,session = session,page=page,limit=limit)


@router.get("/salling_for_you")
async def salling_for_games_you(user:str,page:int=Query(default=1,gt=0),limit:int=Query(default=100,gt=-1),analitic_service = Depends(get_analitic_service),session = Depends(get_async_db)):
    return await analitic_service.salling_for_you_games(user=user,session=session,page=page,limit=limit)


@router.get("/user_achivements")
async def user_achivements(steam_id:str, app:str,session=Depends(get_async_db),analitic_service = Depends(get_analitic_service)):
    return await analitic_service.user_achivements(steam_id,app,session=session)


@router.get("/free_games")
async def free_games(analitic_service=Depends(get_analitic_service),session=Depends(get_async_db)):
    result = await analitic_service.free_games(session=session)
    if result:
        return result
    else:
        return JSONResponse(
            status_code=200,
            content={"detail":False}
        )


@router.get("/random_games")
async def random_games(analitic_service=Depends(get_analitic_service),session=Depends(get_async_db)):
    return await analitic_service.random_games(session=session,limit=1)


@router.get("/game_price_now/{app}")
async def game_price_now(app:str,analitic_service=Depends(get_analitic_service),session=Depends(get_async_db)):
    return await analitic_service.game_price_now(app=app,session=session)