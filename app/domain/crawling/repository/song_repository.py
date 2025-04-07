from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from ..model.song import Song

class SongRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def insert_songs(self, songs: List[Song]) -> None:
        """여러 곡을 한 번에 데이터베이스에 저장합니다."""
        try:
            stmt = insert(Song).values([{
                'rank': song.rank,
                'title': song.title,
                'artist': song.artist
            } for song in songs])
            
            await self._session.execute(stmt)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise Exception(f"노래 저장 중 오류 발생: {str(e)}")

    async def insert_song(self, rank: int, title: str, artist: str) -> None:
        """단일 곡을 데이터베이스에 저장합니다."""
        try:
            stmt = insert(Song).values(
                rank=rank,
                title=title,
                artist=artist
            )
            
            await self._session.execute(stmt)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise Exception(f"노래 저장 중 오류 발생: {str(e)}")
