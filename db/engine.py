from typing import Union

from sqlalchemy import MetaData
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from config import DataBase


def create_engine(url: Union[URL, str]) -> AsyncEngine:
    return create_async_engine(url=url)


async def create_schema(engine: AsyncEngine, metadata: MetaData) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)


def get_async_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, class_=AsyncSession)


db_engine = create_engine(DataBase.url)
db_sessionmaker = get_async_session_maker(db_engine)


def connection(func):
    async def wrapper(*args, **kwargs):
        async with db_sessionmaker() as session:
            return await func(session, *args, **kwargs)

    return wrapper
