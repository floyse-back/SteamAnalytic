from datetime import timedelta, datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


from app.repository.database import Base
from app.core.config import TokenConfig

token_config = TokenConfig()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    email = Column(String, default=None)
    steamid = Column(String, default="")
    steamname = Column(String, default="")

    blacklist_token = relationship("BlackList", back_populates="user", cascade="all,delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all,delete-orphan", lazy="joined") #name changed to refresh_tokens

class RefreshToken(Base):
    __tablename__ = 'refreshtokens'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    refresh_token = Column(String, index=True, nullable=False)
    delete_time = Column(DateTime, default=lambda: (
                datetime.now(timezone.utc) + timedelta(minutes=token_config.refresh_token_expires)).replace(
        tzinfo=None))
    user = relationship("UserModel", back_populates="refresh_tokens")

class BlackList(Base):
    __tablename__ = 'blacklist'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String, index=True, nullable=False)
    expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=token_config.refresh_token_expires))
    reason = Column(String)

    user = relationship("UserModel", back_populates="blacklist_token")
