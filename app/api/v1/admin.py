from fastapi import APIRouter


router = APIRouter()


@router.get("/users_list")
async def users_list():
    pass

@router.get("/users_delete/{user_id}")
async def users_delete(user_id: int):
    pass

