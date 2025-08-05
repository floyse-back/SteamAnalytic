from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.config import SYNC_DATABASE_URL

engine = create_engine(SYNC_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
