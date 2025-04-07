from fastapi import APIRouter
from app.domain.crawling.controller.melon_controller import MelonController

router = APIRouter(prefix="/melon", tags=["melon"])
controller = MelonController()

@router.get("/top100")
async def get_top100():
    """멜론 차트 TOP100을 크롤링합니다."""
    return await controller.get_top100() 