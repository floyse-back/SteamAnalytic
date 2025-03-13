from fastapi import APIRouter
from sqlalchemy.ext.asyncio import async_sessionmaker

from ...database.orm import UsersORM
router = APIRouter(prefix="/auth",tags=["auth"])

users = UsersORM()
AsyncLocalSession = async_sessionmaker(engine=engine, expire_on_commit=False)

@router.post("/login/")
def login_user():
    return {"message":"Login successful"}

@router.get("/logout/")
def logout_user():
    return {"message":"Logout successful"}

@router.post("/register_user")
def register_user(user:User):
    return {"message":"Register successful"}

@router.get("/user/me")
def user_me():
    return {"message":"User Me"}
