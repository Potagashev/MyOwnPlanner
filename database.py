from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from models import Base
from settings import settings

engine = create_async_engine(settings.database_dsn)
SessionLocal = async_sessionmaker(bind=engine, autoflush=False)

def init_db():
    Base.metadata.create_all(bind=engine)