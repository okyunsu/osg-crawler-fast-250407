from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from ...domain.crawling.model.song import Base
from .database import Database

async def create_tables():
    """데이터베이스 테이블을 생성합니다."""
    engine = Database().engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables()) 