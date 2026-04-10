from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "VicAI Assistant"
    environment: str = "development"
    api_prefix: str = "/api/v1"

    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60 * 24

    openai_api_key: str = ""
    llm_default_model: str = "gpt-4.1-mini"
    llm_deep_model: str = "gpt-4.1"
    llm_fast_model: str = "gpt-4.1-mini"

    embeddings_model: str = "text-embedding-3-small"
    database_url: str = "sqlite:///./viciai.db"
    knowledge_path: str = "app/data/knowledge"

    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
