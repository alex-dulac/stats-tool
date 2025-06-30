import csv
from pathlib import Path
from typing import Optional, AsyncGenerator

from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlmodel import SQLModel, select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from server.app import settings

# Models to register with SQLModel.metadata
from server.app.models import Stats


class SessionManager:
    def __init__(self) -> None:
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    async def init_db(self) -> None:
        database_url = (
            f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
            f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )

        self.engine = create_async_engine(
            database_url,
            poolclass=AsyncAdaptedQueuePool,
            pool_pre_ping=True,
        )

        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession
        )

        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        await self.load_initial_data()

    async def close_db(self) -> None:
        if self.engine:
            await self.engine.dispose()

    async def load_initial_data(self) -> None:
        async with self.session_factory() as session:
            result = await session.exec(select(func.count()).select_from(Stats))
            count = result.first()

            if count == 0:
                # Table is empty, load data from CSV
                csv_file_path = Path(__file__).parent.parent / 'data' / 'stats.csv'

                with open(csv_file_path, 'r') as csvfile:
                    csv_reader = csv.DictReader(csvfile)
                    for row in csv_reader:
                        # example "100:50" , "minutes:seconds", convert to total seconds
                        toi_parts = row['toi'].rstrip('.').split(':')
                        toi_seconds = int(toi_parts[0]) * 60 + int(toi_parts[1])

                        stat = Stats(
                            season=int(row['season']),
                            player_name=row['player_name'],
                            team=row['team'],
                            gp=int(row['gp']),
                            toi=toi_seconds,
                            shots=int(row['shots']),
                            goals=int(row['goals']),
                            assists=int(row['assists']),
                            points=int(row['points']),
                            scouting_grade=int(row['scouting_grade'])
                        )
                        session.add(stat)

                await session.commit()


session_manager = SessionManager()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if not session_manager.session_factory:
        raise RuntimeError("Database session factory is not initialized.")
    async with session_manager.session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
