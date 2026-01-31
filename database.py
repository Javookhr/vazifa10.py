import os
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase

DB_URL = "sqlite+aiosqlite:///./main.db"
engine = create_async_engine(DB_URL,echo=True)
LocalSession = async_sessionmaker(engine,expire_on_commit=False)

class Base(DeclarativeBase):
    pass 

async def get_db():
    async with LocalSession() as session:
        yield session
        
MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR,exist_ok=True)