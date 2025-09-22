from fastapi import Header, HTTPException
from typing import Union

from loader import JWTManager, DBAdapter
from models import Users


async def get_jwt_user(authorization: str = Header(...)) -> Union[None, Users]:
    """
    Получение текущего пользователя из JWT токена
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]

    payload = JWTManager.decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await DBAdapter.get_user_by_username(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user