from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from sqlalchemy.engine import Engine

from aiosqlite import Connection

from typing import Any


class BaseDB:
    def __init__(self, tables: Any, db_url: str, logger: Any):
        self.tables = tables
        self._engine_ = create_async_engine(db_url)
        self._session_: sessionmaker[AsyncSession] = sessionmaker(
            self._engine_, 
            class_=AsyncSession
        )
        self.logger = logger

        
    async def init_tables(self) -> None: 
        """
        Инициализирует все таблицы в бд, используя метаданные.
        """
        async with self._engine_.begin() as conn:
            await conn.run_sync(self.tables.metadata.create_all)
        self.logger.info("database initialized")

    @staticmethod
    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection: Any, connection_record: Any) -> None: 
        """
        Включение foreign_keys для sqlite
        """
        if isinstance(dbapi_connection, Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()