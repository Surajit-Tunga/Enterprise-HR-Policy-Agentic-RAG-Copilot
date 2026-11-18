from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Enterprise HR Policy & Employee Support Agentic RAG Copilot"
    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8080

    openai_api_key: str = ""
    tavily_api_key: str = ""
    pinecone_api_key: str = ""
    pinecone_index_name: str = "fde-hr-policy-rag"
    pinecone_namespace: str = "company-hr-kb"
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    top_k: int = 4
    max_retries: int = 1
    admin_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
