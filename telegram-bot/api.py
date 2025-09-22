from aiohttp import ClientSession
from sqlalchemy import select, update, delete

from typing import (
    Any, 
    Dict, 
    Optional, 
    Union, 
    List
)

from models import BaseDB, User, URL
from loader import password_len
from enums import GetToken, HTTPMethod
from utils import format_username, generate_password, get_exp_datetime
from errors import (
    UserAlreadyExist, 
    UserInvalidPassword, 
    NoURL, 
    AddURLError
)

from datetime import datetime, timezone


class MultiClient(BaseDB):
    def __init__(self, api_url: str, **kwargs: Any):
        super().__init__(**kwargs)

        self.api_url = api_url


    async def get_urls(self, id: int) -> Dict[Any, Any]:
        resp = await self.make_request(
            id = id, 
            method = "urls",
            http_method = HTTPMethod.get
        )
        return resp['result']
    
    async def add_url(self, id: int, url: str, interv: int) -> bool:
        resp = await self.make_request(
            id = id, 
            method = "urls",
            http_method = HTTPMethod.post,
            payload = {
                "url": url,
                "interval": interv
            }
        )
        if 'detail' in resp:
            raise AddURLError(message=resp['detail'])

        await self._add_url_db(id=resp['result'], userid=id, interval=interv)
        return True

    async def get_history(
            self, 
            id: int, 
            url: int, 
            limit: Optional[int] = None
    ) -> Dict[str, List[Dict[str, str]]]:
        resp = await self.make_request(
            id = id,
            method = f"history",
            http_method = HTTPMethod.get,
            payload={
                "id": url, "limit": limit
            }
        )
        if 'detail' in resp:
            raise NoURL(message=resp['detail'])
        return resp['result']
    
    async def get_url(self, id: int, url: int) -> ...:
        resp = await self.make_request(
            id = id,
            method = f"urls/{url}",
            http_method = HTTPMethod.get
        )
        if 'detail' in resp:
            raise NoURL(message=resp['detail'])
        return resp['result']
    
    async def update_interval(self, id: int, url: int, interv: int) -> bool:
        resp = await self.make_request(
            id = id,
            method = f'urls/{url}',
            http_method = HTTPMethod.patch,
            payload = {"interval": interv}
        )
        if 'detail' in resp:
            raise NoURL(message=resp['detail'])
        return True

    async def delete_url(self, id: int, url: int) -> Union[str, bool]:
        resp = await self.make_request(
            id = id,
            method = f"urls/{url}",
            http_method = HTTPMethod.delete
        )
        if 'detail' in resp:
            raise NoURL(message=resp['detail'])
        
        await self._delete_url_db(url_id=url, id=id)
        return True

    async def _get_user_db(self, id: int) -> User:
        async with self._session_() as session:
            data = await session.execute(
                select(User)
                .where(User.username == format_username(id=id))
            )
            data = data.scalar()
            if data:
                data.password = self.decrypt(data.password)
                data.jwt_token = self.decrypt(data.jwt_token)
                data.refresh_token = self.decrypt(data.refresh_token)
            return data
        
    def url(self, method: str) -> str:
        return f"{self.api_url}/{method}"

    async def make_request(
            self,
            id: int,
            method: str,
            http_method: str,
            payload: Optional[Dict[str, Any]] = {},
            force: Optional[bool] = False
    ) -> Dict[Any, Any]:
        headers = {}
        if not force:
            user = await self._get_user_db(id=id)
            if not user:
                token = await self._register_user(id=id)
            else:
                tokens = self.check_tokens(user.jwt_token, user.refresh_token)
                match tokens:
                    case GetToken.need_new:
                        token = await self._get_new_token(user=user)
                    case GetToken.need_refresh:
                        token = await self._refresh_token(user=user)
                    case GetToken.ok:
                        token = user.jwt_token

            headers = self.get_headers(token = token)
        async with ClientSession() as session:
            async with session.request(
                http_method, 
                self.url(method=method), 
                json=payload, 
                headers = headers
            ) as response:
                return await response.json(content_type=None)
            
    async def _get_new_token(self, user: User) -> str:
        response = await self.make_request(
            id = user.username,
            payload = {
                "username": user.username,
                "password": self.decrypt(user.password)
            },
            method = "token",
            http_method = HTTPMethod.post,
            force=True
        )
        if response.get("detail") == "Invalid credentials":
            raise UserInvalidPassword(
                message = f"bad password in db for user {user.username}"
                )
        await self._upload_tokens_db(
            jwt_token=response['access_token'], 
            refresh_token=response['refresh_token'], 
            username=user.username
        )
        return response['access_token']
    
    async def _refresh_token(self, user: User) -> str:
        response = await self.make_request(
            id = user.username,
            payload = {"refresh_token": user.refresh_token},
            method = "refresh",
            http_method = HTTPMethod.post,
            force=True
        )
        if response.get("detail") == "Invalid credentials":
            raise UserInvalidPassword(
                message = f"bad password in db for user {user.username}"
                )
        await self._upload_tokens_db(
            jwt_token=response['access_token'], 
            refresh_token=response['refresh_token'], 
            username=user.username
        )
        return response['access_token']

    async def _upload_tokens_db(self, jwt_token: str, refresh_token: str, username: str) -> None:
        payload = {}
        if jwt_token:
            payload[User.jwt_token.key] = self.encrypt(jwt_token)
        if refresh_token:
            payload[User.refresh_token.key] = self.encrypt(refresh_token)

        async with self._session_() as session:
            await session.execute(
                update(User)
                .where(User.username == username)
                .values(**payload)
            )
            await session.commit()

    @staticmethod
    def get_headers(token: str) -> Dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    @staticmethod
    def check_tokens(access_token: str, refresh_token: str) -> str:
        now = datetime.now(timezone.utc) 

        access_exp = get_exp_datetime(token=access_token)
        if access_exp and access_exp > now:
            return GetToken.ok

        refresh_exp = get_exp_datetime(token=refresh_token)
        if refresh_exp and refresh_exp > now:
            return GetToken.need_refresh

        return GetToken.need_new


    async def _register_user(self, id: int) -> str:
        passw =  generate_password(len=password_len)
        response = await self.make_request(
            id = id,
            payload = {
                "username": format_username(id=id),
                "password": passw
            },
            method = "register",
            http_method = HTTPMethod.post,
            force = True
        )
        if response.get("detail") == "User already exists":
            raise UserAlreadyExist(format_username(id=id))
        await self._add_user_db(
            username=format_username(id=id),
            password=passw,
            jwt_token=response['access_token'],
            refresh_token=response['refresh_token']
        )
        return response['access_token']

    async def _add_user_db(
            self, 
            username: str,
            password: str,
            jwt_token: str,
            refresh_token: str
    ) -> None:
        async with self._session_() as session:
            session.add(User(
                username = username,
                password = self.encrypt(password),
                jwt_token = self.encrypt(jwt_token),
                refresh_token = self.encrypt(refresh_token)
            ))
            await session.commit()

    async def _get_urls_track(self) -> List[URL]:
        async with self._session_() as session:
            data = await session.execute(
                select(URL)
            )
            return data.scalars()
        
    async def _delete_url_db(self, url_id: int, id: int) -> None:
        async with self._session_() as session:
            await session.execute(
                delete(URL)
                .where(
                    (URL.username == format_username(id=id)) & (URL.id == url_id)
                ))
            await session.commit()

    async def _add_url_db(self, id: int, userid: int, interval: int) -> None:
        async with self._session_() as session:
            session.add(URL(
                id = id,
                username = format_username(id=userid),
                interval = interval
            ))
            await session.commit()