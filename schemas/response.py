from pydantic import BaseModel, Field
from typing import Optional

class SQLResponse(BaseModel):
    """SQL响应模型"""
    sql: str = Field(
        ...,
        description="Generated SQL statement"
    )
    success: bool = Field(
        ...,
        description="Whether the conversion was successful"
    )
    message: Optional[str] = Field(
        None,
        description="Additional information or error message"
    )