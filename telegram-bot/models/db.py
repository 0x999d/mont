from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from typing import Any

from aes import CipherAES


class BaseDB(CipherAES):
    def __init__(
            self, tables: Any, 
            db_url: str, logger: Any, 
            chiper_key: str
        ):
        super().__init__(key=chiper_key)
        self.tables = tables
        self._engine_ = create_async_engine(db_url)
        self._session_: sessionmaker[AsyncSession] = sessionmaker(
            self._engine_, 
            class_=AsyncSession
        )
        self.logger = logger
        
    async def init_tables(self) -> None: 
        """
        Инициализирует все таблицы в бд, используя метаданные
        """
        async with self._engine_.begin() as conn:
            await conn.run_sync(self.tables.metadata.create_all)
        self.logger.info("database initialized")