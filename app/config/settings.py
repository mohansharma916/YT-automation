from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Youtube AI Agent"

    log_level: str = "INFO"
    openai_api_key: str

    transcription_model: str = "whisper-1"

    chat_model: str = "gpt-4.1-mini"
    deepgram_api_key: str
    sarvam_api_key: str
    sarvam_base_url: str
    transcription_provider: str = "openai"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()