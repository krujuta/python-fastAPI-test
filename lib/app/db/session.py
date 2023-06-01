from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.app.core.config import settings

engine = create_engine(settings.SESSION_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
