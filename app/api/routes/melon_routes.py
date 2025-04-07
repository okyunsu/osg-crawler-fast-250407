from fastapi import APIRouter, HTTPException
from app.domain.crawling.controller.melon_controller import MelonController
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/melon", tags=["melon"])
controller = MelonController()

@router.get("/top100")
async def get_top100():
    """멜론 차트 TOP100을 크롤링합니다."""
    try:
        logger.info("Starting to crawl Melon TOP100")
        result = await controller.get_top100()
        logger.info(f"Successfully crawled {len(result.get('songs', []))} songs")
        return result
    except Exception as e:
        logger.error(f"Failed to crawl Melon TOP100: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 