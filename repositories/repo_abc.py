from abc import ABC
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker

class RepositoryABC(ABC):
    __table__ = None

    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory

    @asynccontextmanager
    async def unit_of_work(self):
        async with self.session_factory() as session, session.begin():
            try:
                yield session
            except Exception:
                raise
