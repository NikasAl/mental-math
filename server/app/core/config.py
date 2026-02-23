from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


# Get the server directory (where .env is located)
SERVER_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    # Database
    mm_database_url: str = "sqlite+aiosqlite:///./mental_math.db"

    # JWT
    mm_jwt_secret_key: str = "your-super-secret-key-change-in-production"
    mm_jwt_algorithm: str = "HS256"
    mm_access_token_expire_minutes: int = 1440  # 24 hours

    # OpenRouter
    mm_openrouter_api_key: str = ""

    # App
    mm_debug: bool = True
    mm_api_v1_prefix: str = "/api/v1"

    class Config:
        env_file = str(SERVER_DIR / ".env")
        env_file_encoding = "utf-8"
        
    @property
    def database_url(self) -> str:
        return self.mm_database_url
    
    @property
    def jwt_secret_key(self) -> str:
        return self.mm_jwt_secret_key
    
    @property
    def jwt_algorithm(self) -> str:
        return self.mm_jwt_algorithm
    
    @property
    def access_token_expire_minutes(self) -> int:
        return self.mm_access_token_expire_minutes
    
    @property
    def openrouter_api_key(self) -> str:
        return self.mm_openrouter_api_key
    
    @property
    def debug(self) -> bool:
        return self.mm_debug
    
    @property
    def api_v1_prefix(self) -> str:
        return self.mm_api_v1_prefix


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
