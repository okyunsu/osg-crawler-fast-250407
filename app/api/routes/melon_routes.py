from fastapi import APIRouter, HTTPException, Request
from app.domain.crawling.controller.melon_controller import MelonController
import logging
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(prefix="/melon", tags=["melon"])
controller = MelonController()

@router.get("/top100")
async def get_top100(request: Request):
    """멜론 차트 TOP100을 크롤링합니다."""
    request_id = id(controller)
    client_host = request.client.host if request.client else "unknown"
    
    logger.info(f"[{request_id}] Received request from {client_host}")
    
    try:
        logger.info(f"[{request_id}] Starting to crawl Melon TOP100")
        result = await controller.get_top100()
        
        if not result or not isinstance(result, dict):
            logger.error(f"[{request_id}] Invalid result format: {result}")
            raise HTTPException(status_code=500, detail="크롤링 결과가 올바르지 않습니다.")
        
        songs_count = len(result.get('songs', []))
        logger.info(f"[{request_id}] Successfully crawled {songs_count} songs")
        
        if songs_count == 0:
            logger.warning(f"[{request_id}] No songs were crawled")
            raise HTTPException(status_code=500, detail="크롤링된 노래가 없습니다.")
        
        return result
        
    except HTTPException as he:
        logger.error(f"[{request_id}] HTTP Exception: {str(he)}")
        raise
        
    except Exception as e:
        error_trace = traceback.format_exc()
        logger.error(f"[{request_id}] Failed to crawl Melon TOP100: {str(e)}\n{error_trace}")
        raise HTTPException(
            status_code=500,
            detail=f"크롤링 중 오류가 발생했습니다: {str(e)}"
        ) 