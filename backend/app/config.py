"""
Configuration management for RoutAIne backend.

Loads environment variables and provides application settings.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Application
    APP_NAME: str = "RoutAIne"
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-change-in-production"

    # Database
    MONGODB_URL: str = "mongodb://localhost:27017/routaine"
    DATABASE_NAME: str = "routaine"

    # API Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]

    # OpenAI Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 2000

    # Twilio Configuration
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    # Service Configuration
    TASK_DEFAULT_DURATION: int = 60  # minutes
    MAX_TASKS_PER_DAY: int = 20
    NOTIFICATION_RETRY_ATTEMPTS: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
