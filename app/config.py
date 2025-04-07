from pydantic import BaseSettings

class Settings(BaseSettings):
    CRAWLING_MODE: str = "internal"
    ENV: str = "local"

    class Config:
        env_file = ".env"

settings = Settings()
