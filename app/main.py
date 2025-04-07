from fastapi import FastAPI
from app.config import settings
from app.crawling.internal import crawl_internal
from app.crawling.external import crawl_external

app = FastAPI()

@app.get("/crawl")
def crawl():
    if settings.CRAWLING_MODE == "external":
        return crawl_external()
    else:
        return crawl_internal()
