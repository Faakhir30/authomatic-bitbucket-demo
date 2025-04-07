from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""

    # BitBucket OAuth 1.0a
    bb_key_legacy: str = os.getenv("BB_KEY_LEGACY", "")
    bb_secret_legacy: str = os.getenv("BB_SECRET_LEGACY", "")

    # BitBucket OAuth 2.0
    bb_client_id: str = os.getenv("BB_CLIENT_ID", "")
    bb_client_secret: str = os.getenv("BB_CLIENT_SECRET", "")
    bb_workspace: str = os.getenv("BB_WORKSPACE", "")

    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # App Settings
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    host: str = os.getenv("HOST", "localhost")
    port: int = int(os.getenv("PORT", "8000"))

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()


# OAuth Configuration
OAUTH_CONFIG = {
    "bitbucket_legacy": {
        "class_": "authomatic.providers.oauth1.Bitbucket",
        "consumer_key": get_settings().bb_key_legacy,
        "consumer_secret": get_settings().bb_secret_legacy,
    },
    "bitbucket_modern": {
        "class_": "app.providers.BitbucketOAuth2",
        "consumer_key": get_settings().bb_client_id,
        "consumer_secret": get_settings().bb_client_secret,
        "scope": ["repository", "team", "account"],
        "workspace": get_settings().bb_workspace,
    },
}
