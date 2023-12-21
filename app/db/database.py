""" Настройка БД """
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# создание движка БД
engine = create_async_engine(settings.ASYNC_DATABASE_URL)
# передача нашего движка в создатель сессий
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass
