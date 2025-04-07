from fastapi import APIRouter, HTTPException
from app.domain.crawling.controller.melon_controller import MelonController
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(prefix="/melon", tags=["melon"])
controller = MelonController()

@router.get("/top100")
async def get_top100():
    """멜론 차트 TOP100을 크롤링합니다."""
    request_id = id(controller)  # 각 요청을 구분하기 위한 ID
    try:
        logger.info(f"[{request_id}] Starting to crawl Melon TOP100")
        result = await controller.get_top100()
        songs_count = len(result.get('songs', []))
        logger.info(f"[{request_id}] Successfully crawled {songs_count} songs")
        logger.debug(f"[{request_id}] Crawling result: {result}")
        return result
    except Exception as e:
        logger.error(f"[{request_id}] Failed to crawl Melon TOP100: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"크롤링 중 오류가 발생했습니다: {str(e)}"
        ) 