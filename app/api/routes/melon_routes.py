from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.crawling import controller
from ...domain.crawling.service.melon_service import MelonService
from ...foundation.infra.database.database import get_db
import logging
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(prefix="/melon", tags=["melon"])

@router.get("/top100")
async def get_top100(session: AsyncSession = Depends(get_db)):
    """멜론 차트 TOP100을 크롤링하여 반환합니다."""
    try:
        service = MelonService(session)
        songs = await service.crawl_top100()
        return {
            "status": "success",
            "data": [{"rank": song.rank, "title": song.title, "artist": song.artist} for song in songs]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top100_old")
async def get_top100_old(request: Request):
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