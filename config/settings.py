from pydantic import Field,validator
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict
import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

# 全局配置
class Settings(BaseSettings):
    # 交互配置
    CONSOLE_INPUT: bool = Field(default=False) # 是否采用控制台交互模式, 默认False, 即默认采用对外暴露接口的方式进行HTTP交互
    # 数据库配置
    DATA_BASE_TYPE: str = Field(default='MYSQL') # 使用的数据库, 默认MYSQL

    # Redis配置
    ENABLE_REDIS: bool = Field(default=True) # 是否开启Redis, 默认开启
    REDIS_HOST: str = Field(default="localhost") # redis的主机地址
    REDIS_PORT: int = Field(default=6379) # redis端口
    REDIS_DB: int = Field(default=0) # redis使用的DB
    REDIS_PASSWORD: Optional[str] = Field(default=None) # redis密码(一般是没有的)
    REDIS_TTL: int = Field(default=3600)  # 缓存过期时间（秒）

    # Agent配置
    OPENAI_API_KEY: str = Field(default="") # OPENAI_API_KEY, 懂的都懂
    MODEL_NAME: str = Field(default="gpt-4o-mini") # 使用的模型名称, 推荐reasoning model
    ENABLE_OPTIMIZE_AGENT: bool = Field(default=False) # 是否开启优化SQL的智能体

    # Team配置
    ENABLE_SELECTOR_TEAM: bool = Field(default=False) # 是否使用SelectTeam, 默认使用RobinRoundGroupChat作为Team
    MAX_CONTEXT_MESSAGES: int = Field(default=8) # 最大上下文消息数

    @validator('MAX_CONTEXT_MESSAGES')
    def ensure_min_max_context_messages(cls, v): # 保证上下文消息数至少为8条, 防止异常终止
        return max(v, 8)

    # SQL建表语句的存放地址 (暂不支持相对地址, 仅支持从盘符开始的绝对地址)
    SQL_FILE_PATH: str = Field(default="resource")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache
def get_settings():
    """缓存设置实例以避免重复加载"""
    return Settings()