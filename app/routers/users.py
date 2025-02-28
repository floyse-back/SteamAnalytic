from fastapi import APIRouter
from starlette import status

router = APIRouter()

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register_user():
    return {"message": "Register user"}

@router.post("/login",status_code=status.HTTP_201_CREATED)
async def login_user():
    return {"message": "Login user"}

@router.put("/change_user_data",status_code=status.HTTP_202_ACCEPTED)
async def change_user_data():
    return {"message": "Change user data"}

@router.delete("/delete_user",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user():
    return {"message": "Delete user"}