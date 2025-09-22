from fastapi import APIRouter
from fastapi import HTTPException

from loader import DBAdapter, JWTManager
from models import Token, Auth, TokenRefresh


router = APIRouter()

@router.post("/register", response_model=Token)
async def register(data: Auth):
    """
    Регистрация новых пользователей
    """
    user = await DBAdapter.register_user(
        password=data.password, 
        user=data.username
)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    access_token = JWTManager.create_access_token(data={"sub": data.username})
    refresh_token = JWTManager.create_refresh_token(data={"sub": data.username})
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/token", response_model=Token)
async def login(data: Auth):
    """
    Получение JWT токена
    """
    user = await DBAdapter.get_user_by_username(data.username)
    if not user or not DBAdapter.CryptManager.verify_hashes(
        user.password,
        data.password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = JWTManager.create_access_token(data={"sub": user.username})
    refresh_token = JWTManager.create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh", response_model=Token)
async def refresh_token(data: TokenRefresh):
    """
    Обновление JWT токенов
    """
    payload = JWTManager.decode_token(data.refresh_token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    username = payload["sub"]
    access_token = JWTManager.create_access_token(data={"sub": username})
    refresh_token = JWTManager.create_refresh_token(data={"sub": username})
    return {"access_token": access_token, "refresh_token": refresh_token}