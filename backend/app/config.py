from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./goldcert.db"
    JWT_SECRET: str = "dev-secret"
    UPLOAD_FOLDER: str = str(Path(__file__).resolve().parent / "uploads")
    MAX_CONTENT_LENGTH: int = 50 * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    Path(settings.UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
    return settings
