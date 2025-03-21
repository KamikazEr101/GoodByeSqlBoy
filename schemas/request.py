from pydantic import BaseModel, Field
from typing import Optional

class NLQueryRequest(BaseModel):
    """自然语言查询请求模型"""
    query: str = Field(
        ...,
        min_length=1,
        description="Natural language query to be converted to SQL"
    )