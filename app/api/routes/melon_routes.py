from fastapi import APIRouter
from app.domain.crawling.controller.melon_controller import MelonController

router = APIRouter(prefix="/melon", tags=["melon"])
controller = MelonController()

@router.get("/top100")
async def get_top100():
    """멜론 차트 TOP100을 크롤링합니다."""
    return controller.get_top100()

@router.get("/latest")
async def get_latest():
    """가장 최근에 크롤링한 노래 목록을 반환합니다."""
    return controller.get_latest_songs() 