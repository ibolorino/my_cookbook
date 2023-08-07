from sqlmodel import Session, create_engine

from my_cookbook.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URI)

local_session = Session(autocommit=False, autoflush=False, bind=engine)
