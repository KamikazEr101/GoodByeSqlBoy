from pydantic import Field,validator
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict
import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

# 全局配置
class Settings(BaseSettings):
    # 数据库配置
    DATA_BASE_TYPE: str = Field(default='MYSQL')

    # API配置
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "GoodbyeSqlBoy"

    # Redis配置
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)
    REDIS_PASSWORD: Optional[str] = Field(default=None)
    REDIS_KEY_PREFIX: str = Field(default="gsb:")
    REDIS_TTL: int = Field(default=3600)  # 缓存过期时间（秒）

    # Agent配置
    OPENAI_API_KEY: str = Field(default="")
    ENABLE_OPTIMIZE_AGENT: bool = Field(default=True)

    # Team配置
    ENABLE_SELECTOR_TEAM: bool = Field(default=False)
    MAX_CONTEXT_MESSAGES: int = Field(default=8)

    @validator('MAX_CONTEXT_MESSAGES')
    def ensure_min_max_context_messages(cls, v):
        return max(v, 8)

    # 性能调优
    MAX_RETRIES: int = Field(default=3)
    TIMEOUT: int = Field(default=30)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    SQL_FILE_PATH: str = Field(default="resource")

@lru_cache
def get_settings():
    """缓存设置实例以避免重复加载"""
    return Settings()