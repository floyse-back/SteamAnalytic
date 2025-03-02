from fastapi import APIRouter

router = APIRouter()


@router.get("/analytics")
async def analytics():
    return {"message": "Hello World"}

@router.get("/friends_top_games")
async def friends_top_games():
    return {"message": "Hello World"}

@router.get("/popular_games/")
async def popular_games(ganre: str=None):
    return {"message": "popular games"}

@router.get("/friends_activity_track")
async def friends_activity_track():
    return {"message": "friends activity track"}

@router.get("/friend_game_list/")
async def friend_game_list(user_id: int=None):
    return {"message": "friend game list"}

