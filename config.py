
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    DATABASE_URL: str
    APP_NAME: str = "Food AI API"
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
