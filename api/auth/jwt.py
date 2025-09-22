from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


class JWT:
    def __init__(
        self,
        public_key_path: str,
        private_key_path: str,
        access_token_exp_minutes: int = 30,
        refresh_token_exp_days: int = 7,
    ):
        self.public_key = self.load_key(public_key_path)
        self.private_key = self.load_key(private_key_path)
        self.access_token_exp_minutes = access_token_exp_minutes
        self.refresh_token_exp_days = refresh_token_exp_days
        self.algo = "RS256"

    @staticmethod
    def load_key(path: str) -> str:
        """
        Загружает RSA ключ из файла по пути
        """
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def create_access_token(self, data: dict, expires: timedelta = None):
        """
        Создаёт JWT access token
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires or timedelta(minutes=self.access_token_exp_minutes)
        )
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.private_key, algorithm=self.algo) 

    def create_refresh_token(self, data: dict, expires: timedelta = None):
        """
        Создаёт JWT refresh token
        """
        to_encode = data.copy() 
        expire = datetime.now(timezone.utc) + (
            expires or timedelta(days=self.refresh_token_exp_days)
        )
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, self.private_key, algorithm=self.algo)
 
    def decode_token(self, token: str):
        """
        Декодирует JWT, возвращает payload или None при ошибке
        """
        try:
            payload = jwt.decode(token, self.public_key, algorithms=[self.algo])
            return payload
        except JWTError:
            return None