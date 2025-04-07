from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from ..model.song import Song
from ..repository.song_repository import SongRepository

class MelonService:
    """멜론 차트 크롤링 서비스"""
    
    def __init__(self, session: AsyncSession):
        self.repository = SongRepository(session)
        self.url = "https://www.melon.com/chart/index.htm"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    async def crawl_top100(self) -> List[Song]:
        """멜론 차트 TOP100을 크롤링합니다."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=self.headers) as response:
                    response.raise_for_status()
                    html = await response.text()
            
            soup = BeautifulSoup(html, 'html.parser')
            songs = []
            
            for rank, row in enumerate(soup.select('tbody tr'), 1):
                title = row.select_one('.rank01 span a').text.strip()
                artist = row.select_one('.rank02 span a').text.strip()
                
                song = Song(rank=rank, title=title, artist=artist)
                songs.append(song)
            
            # 크롤링한 데이터를 DB에 저장
            await self.repository.insert_songs(songs)
            
            return songs
            
        except Exception as e:
            raise Exception(f"크롤링 중 오류가 발생했습니다: {str(e)}")
    
    async def save_song(self, rank: int, title: str, artist: str) -> None:
        """단일 곡을 데이터베이스에 저장합니다."""
        await self.repository.insert_song(rank, title, artist)
    
    def get_latest_songs(self) -> List[Dict]:
        """가장 최근에 크롤링한 노래 목록을 반환합니다."""
        return self.repository.get_latest_songs()
    
    def get_songs_by_date(self, date: datetime) -> List[Dict]:
        """특정 날짜의 노래 목록을 반환합니다."""
        return self.repository.get_songs_by_date(date) 