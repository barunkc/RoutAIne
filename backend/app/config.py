from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "routAIne API"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "routaine"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_from_number: str = ""
    twilio_to_number: str = ""
    sms_worker_interval_seconds: int = 60
    routine_generator_interval_seconds: int = 300
    habit_tracker_interval_seconds: int = 600

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
