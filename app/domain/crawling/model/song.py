from sqlalchemy import Column, Integer, String
from app.foundation.infra.database.database import Base

class Song(Base):
    """멜론 차트 노래 정보 모델"""
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rank = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)

    def __repr__(self):
        return f"<Song(rank={self.rank}, title='{self.title}', artist='{self.artist}')>" 