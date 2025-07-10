from datetime import timedelta, datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship


from app.infrastructure.db.database import Base
from app.utils.config import TokenConfig

token_config = TokenConfig()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    email = Column(String, default=None)
    is_active = Column(Boolean, default=False)
    role = Column(String, default="user")
    steamid = Column(String, default="")
    steamname = Column(String, default="")

    blacklist_token = relationship("BlackList", back_populates="user", cascade="all,delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all,delete-orphan", lazy="joined") #name changed to refresh_tokens
    email_confirmed = relationship("EmailConfirmed",back_populates="user", cascade="all,delete-orphan")

class RefreshToken(Base):
    __tablename__ = 'refreshtokens'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    refresh_token = Column(String, index=True, nullable=False)
    delete_time = Column(DateTime, default=lambda: (
                datetime.now() + timedelta(minutes=token_config.refresh_token_expires)))
    user = relationship("UserModel", back_populates="refresh_tokens")

class BlackList(Base):
    __tablename__ = 'blacklist'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String, index=True, nullable=False)
    expires_at = Column(DateTime, default=lambda: datetime.now() + timedelta(minutes=token_config.refresh_token_expires))
    reason = Column(String)

    user = relationship("UserModel", back_populates="blacklist_token")

class EmailConfirmed(Base):
    __tablename__ = "email_confirmation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    token = Column(String, index=True, nullable=False)
    expires_at = Column(DateTime,default=lambda: datetime.now() + timedelta(minutes=10))

    user_id = Column(ForeignKey("users.id"))
    user = relationship("UserModel",back_populates="email_confirmed")