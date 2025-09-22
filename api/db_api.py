from sqlalchemy import select, delete, update, desc

from typing import Any, Union, Optional, List
from models import TrackedUrls, TrackHistory, BaseDB, Users
from auth import Crypto
from sqlalchemy.orm import selectinload  # или joinedload

class DBAPI(BaseDB):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.CryptManager = Crypto()

    async def get_urls(
            self, 
            username: Optional[str] = None, 
            url: Optional[str] = None,
            id: Optional[int] = None
            ) -> List[Union[TrackedUrls, None]]:
        if username and url and not id:
            cmd = (
                select(TrackedUrls)
                .where((TrackedUrls.owner == username) & (TrackedUrls.url == url))
            )
        elif username and not url and not id:
            cmd = select(TrackedUrls).where(TrackedUrls.owner == username)
        elif not username and not url and not id:
            cmd = select(TrackedUrls)
        else:
            cmd = (
                select(TrackedUrls)
                .where((TrackedUrls.owner == username) & (TrackedUrls.id == id))
            )

        async with self._session_() as session:
            data = await session.execute(cmd)
            return [buff[0] for buff in data.fetchall()]

    async def add_url_to_scan(
            self, 
            url: str, 
            username: str, 
            interval: Optional[int] = 60
    ) -> Union[TrackedUrls, bool]:
        if not await self.get_urls(url = url, username = username):
            async with self._session_() as session:
                session.add(TrackedUrls(
                        interval = interval,
                        url = url,
                        owner = username
                    ))
                await session.commit()
                self.logger.info(f"new url to track. {url}")
            return True
        return False

    async def push_history(
            self,
            is_ok: bool,
            site_id: int,
            latency: Optional[float] = None,
            hash_content: Optional[str] = None,
            http_status: Optional[int] = None,
    ) -> TrackHistory:
        async with self._session_() as session:
            track = TrackHistory(
                latency = latency,
                http_status = http_status,
                is_ok = is_ok,
                hash_reqbytes = hash_content,
                site_id = site_id
            )
            session.add(track)
            await session.commit()
            return track

    async def change_interval(self, interval: int, username: str, id: int) -> bool:
        if not await self.get_urls(username = username, id = id):
            return False
        async with self._session_() as session:
            await session.execute(
                update(TrackedUrls)
                .where((TrackedUrls.id == id) & (TrackedUrls.owner == username))
                .values({TrackedUrls.interval: interval})
            )
            await session.commit()
            return True

    async def delete_url(self, username: str, id: int) -> bool:
        if not await self.get_urls(username = username, id = id):
            return False
        async with self._session_() as session:
            await session.execute(
                delete(TrackedUrls)
                .where((TrackedUrls.id == id) & (TrackedUrls.owner == username))
            )
            await session.commit()
            return True
        
    async def get_history(self, limit: int, id: int) -> List[TrackHistory]:
        async with self._session_() as session:
            data = (
        select(TrackHistory)
        .options(selectinload(TrackHistory.site)) 
        .where(TrackHistory.site_id == id).limit(limit=limit)
        .order_by(desc(TrackHistory.date))
    )
            result = await session.execute(data)
            return result.scalars().all()
        
    async def get_user(self, token: str) -> Users:
        data = await self._session_().execute(
            select(Users).where(Users.token == token)
        )
        return data.scalar()

    async def register_user(self, password: str, user: str) -> Union[bool, Users]:
        if await self.get_user_by_username(user = user):
            return False
        
        async with self._session_() as session:
            session.add(Users(
                    username = user,
                    password = self.CryptManager.create_hash(password)
                ))
            await session.commit()
        return True

    async def get_user_by_username(self, user: str) -> Users:
        async with self._session_() as session:
            data = await session.execute(
                select(Users)
                .where(Users.username == user)
            )
            return data.scalar()
        
    async def get_history_by_name(self, limit: int, username: str) -> List[TrackHistory]:
        async with self._session_() as session:
            data = (
                select(TrackHistory)
                .join(TrackedUrls)  
                .options(selectinload(TrackHistory.site)) 
                .where(TrackedUrls.owner == username)
                .order_by(desc(TrackHistory.date))
                .limit(limit)
            )
            result = await session.execute(data)
            return result.scalars().all()