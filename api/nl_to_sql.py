from fastapi import HTTPException, status

from config import settings
from schemas.request import NLQueryRequest
from schemas.response import SQLResponse
from core.cache import redis_template
from core.utils import hash_utils
from core.team import sql_generator_team


async def convert_nl_to_sql(query: str) -> str:
    if settings.ENABLE_REDIS:
        key = hash_utils.sha256_encrypt(query.strip())
        if redis_template.exists(key):
            return redis_template.get(key)

    result = await sql_generator_team.generate_sql(query)
    return result


async def process_nl_query(request: NLQueryRequest) -> SQLResponse:
    try:
        sql_statement = await convert_nl_to_sql(request.query)

        return SQLResponse(
            sql=sql_statement,
            success=True,
            message="Successfully converted natural language to SQL"
        )
    except Exception as e:
        return SQLResponse(
            sql="",
            success=False,
            message=f"Error during conversion: {str(e)}"
        )

