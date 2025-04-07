from datetime import datetime, timezone
from typing import Callable
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.routes.melon_routes import router as melon_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

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

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8888) 