from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from my_cookbook.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)