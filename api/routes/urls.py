from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends, 
    status
)
from enums import HTTPProbeCode

from utils import generate_api_answer
from depends import get_jwt_user
from models import Users, NewURL, ChangeInterval
from loader import DBAdapter, HTTPScanner


router = APIRouter()

@router.get("/urls/{id}")
async def get_url(id: int, data: Users = Depends(get_jwt_user)):
    """
    Получение данных текущего пользователя по access_token
    """
    result = {}

    url = await DBAdapter.get_urls(username=data.username, id=id)
    if not url:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "No url with that id"
        )
    result =  {
        "interval": url[0].interval,
        "url": url[0].url,
        "owner": url[0].owner,
        "id": url[0].id
    }
    return generate_api_answer(
        status_code=status.HTTP_200_OK,
        result=result
    )

@router.get("/urls")
async def get_urls(data: Users = Depends(get_jwt_user)):
    """
    Получение данных текущего пользователя по access_token
    """
    result = {}
    for idx, url in enumerate(await DBAdapter.get_urls(username=data.username)):
        result[idx + 1] = {
            "interval": url.interval,
            "url": url.url,
            "owner": url.owner,
            "id": url.id
        }
    
    return generate_api_answer(
        status_code=status.HTTP_200_OK,
        result=result
    )
   
@router.post("/urls")
async def new_url(url: NewURL, data: Users = Depends(get_jwt_user)):
    """
    Создание новой отслеживаемой URL
    """
    result = await HTTPScanner._make_probe(url.url)

    if not isinstance(result, tuple):
        match result:
            case HTTPProbeCode.bad_url:
                detail = "URL is proxibited, or incorrect"
            case HTTPProbeCode.no_ok:
                detail = "URL must be UP while creating"
            case HTTPProbeCode.error:
                detail = "Unknown error, please try again later"

        raise HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE,
            detail
        )

    ok = await DBAdapter.add_url_to_scan(
        url=url.url, 
        username=data.username,
        interval=url.interval
    )
    if not ok:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "You already track that url"
        )
    
    data = await DBAdapter.get_urls(username = data.username, url = url.url)
    return generate_api_answer(
        status_code=status.HTTP_201_CREATED,
        result=data[0].id
    )

@router.delete("/urls/{id}")
async def delete_url(id: int, data: Users = Depends(get_jwt_user)):
    """
    Удаление URL из отслеживаемых
    """
    ok = await DBAdapter.delete_url(
        username=data.username,
        id=id
    )
    if not ok:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "You dont track this url"
        )
    return generate_api_answer(
        status_code=status.HTTP_200_OK,
        result=True
    )

@router.patch("/urls/{id}")
async def change_interval(interval: ChangeInterval, id: int, data: Users = Depends(get_jwt_user)):
    """
    Изменение интервала для отслеживаемого URL
    """
    ok = await DBAdapter.change_interval(
        id=id, 
        username=data.username,
        interval=interval.interval
    )
    if not ok:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "You dont track this url"
        )
    return generate_api_answer(
        status_code=status.HTTP_200_OK,
        result=True
    )