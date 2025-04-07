from typing import Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker        
from sqlalchemy.orm import declarative_base


class Database:
    _instance: Optional['Database'] = None
    _engine = None
    _session_maker = None
    
    def __new__(cls) -> 'Database':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._engine is None:
            DATABASE_URL = "postgresql+asyncpg://postgres:ZpOZUvdKRhYdtwCUdTsjpdQsIOnJqoNc@yamabiko.proxy.rlwy.net:24952/railway"
            self._engine = create_async_engine(
                DATABASE_URL,
                echo=True,  # SQL 쿼리 로깅
                pool_pre_ping=True,  # 연결 확인
                pool_size=5,  # 커넥션 풀 크기
                max_overflow=10  # 최대 초과 커넥션
            )
            self._session_maker = async_sessionmaker(
                self._engine,
                class_=AsyncSession,
                expire_on_commit=False
            )

    @property
    def engine(self):
        return self._engine

    @property
    def session_maker(self):
        return self._session_maker

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """비동기 세션을 반환합니다."""
        async with self._session_maker() as session:
            try:
                yield session
            finally:
                await session.close()

# Base 클래스 정의 (모델 정의에 사용)
Base = declarative_base()

# 데이터베이스 인스턴스 생성
database = Database()

# 의존성 주입을 위한 제너레이터 함수
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 의존성 주입을 위한 데이터베이스 세션 제너레이터"""
    async for session in database.get_session():
        yield session
