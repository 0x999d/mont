from fastapi import (
    APIRouter, 
    Depends, 
    status
)

from utils import generate_api_answer
from depends import get_jwt_user
from models import Users, History
from loader import DBAdapter


router = APIRouter()

@router.get("/history")
async def get_scanner_history_id(
    params: History, 
    data: Users = Depends(get_jwt_user)
):
    """
    Получение результатов http сканнера по URL id
    """
    result = {}
    if params.id:
        history = await DBAdapter.get_history(
            id=params.id, limit = params.limit
        )
    else:
        history = await DBAdapter.get_history_by_name(
            limit = params.limit, 
            username = data.username
        )
    if history:
        for idx, url in enumerate(history):
            if url.site.owner == data.username:
                result[idx + 1] = {
                    "latency": url.latency,
                    "http_status": url.http_status,
                    "is_ok": url.is_ok,
                    "id": url.site_id,
                    "hash_reqbytes": url.hash_reqbytes,
                    "interval": url.site.interval,
                    "url": url.site.url,
                    "date": url.date.timestamp()
                }
    
    return generate_api_answer(
        status_code=status.HTTP_200_OK,
        result=result
    )