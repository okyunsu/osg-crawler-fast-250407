from datetime import datetime, timezone
from typing import Callable
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.api.routes.melon_routes import router as melon_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Melon Chart Crawler API",
    description="멜론 차트 TOP100을 크롤링하는 API",
    version="1.0.0"
)

app.include_router(melon_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_time: Callable[[], str] = lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

@app.get(path="/")
async def home():
    logger.info("Accessing home page")
    return HTMLResponse(content=f"""
<body>
<div style="width: 400px; margin: 50 auto;">
    <h1>멜론 차트 크롤러 API</h1>
    <h2>현재 서버 구동 중입니다.</h2>
    <h3>{current_time()}</h3>
    <p>API 문서: <a href="/docs">/docs</a></p>
    <p>멜론 차트 TOP100: <a href="/melon/top100">/melon/top100</a></p>
</div>
</body>
""")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "path": str(request.url),
            "type": type(exc).__name__
        }
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.debug(f"Response status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request failed: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080) 