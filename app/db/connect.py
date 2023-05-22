from collections.abc import AsyncGenerator

from app.core.config import Settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel


DATABASE_URL = Settings().DB_CONFIG

engine = create_async_engine(DATABASE_URL, echo=True, future=True, poolclass=NullPool)


async def initialize_db_and_tables():
    """Creates the database and tables if they don't exist."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator:
    """Creates a new database session."""
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
