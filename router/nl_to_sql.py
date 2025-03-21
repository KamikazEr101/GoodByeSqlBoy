from fastapi import APIRouter, status
from schemas.request import NLQueryRequest
from schemas.response import SQLResponse
from api.nl_to_sql import process_nl_query

router = APIRouter(
    prefix="/api/v1",
    tags=["nl2sql"],
    responses={404: {"description": "Not found"}},
)

@router.post("/nl2sql", response_model=SQLResponse, status_code=status.HTTP_200_OK)
async def translate_nl_to_sql(request: NLQueryRequest):
    return await process_nl_query(request)