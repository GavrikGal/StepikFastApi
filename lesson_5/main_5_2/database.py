from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (async_sessionmaker, create_async_engine)

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:sosiska12@localhost/mydatabase"


# connect_args только для SQLite
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # Базовый класс для моделей


async def create_all():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
