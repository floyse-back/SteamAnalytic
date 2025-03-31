from datetime import date, timedelta

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database.database import Base
from app.core.config import TokenConfig

token_config = TokenConfig()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, autoincrement=True)
    username = Column(String,nullable=False,unique=True,index=True)
    hashed_password = Column(String,nullable=False)
    email = Column(String,default = None)
    steamid = Column(String,default = "")
    steamname = Column(String,default="")

    refresh_tokens = relationship("TokenBase", back_populates="user", cascade="all,delete-orphan")


class TokenBase(Base):
    __tablename__ = 'refreshtokens'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    user_id = Column(ForeignKey("users.id",ondelete="CASCADE"))
    refresh_token = Column(String,index=True,nullable=False)
    delete_time = Column(Date,default=lambda: date.today() + timedelta(minutes=token_config.refresh_token_expires))

    user = relationship("UserModel", back_populates="refresh_tokens")
