from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CHROMA_DB_DIR: str = "app/data/vector_store"
    COLLECTION_NAME: str = "yakuza_guide"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    OLLAMA_MODEL: str = "llama3"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()