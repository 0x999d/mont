from aiohttp.client_exceptions import ConnectionTimeoutError
from aiohttp import ClientSession

from typing import Tuple, Union, Any

from hashlib import sha256
from time import perf_counter
from re import sub, fullmatch

from datetime import datetime, timedelta
from asyncio import run

from models import TrackedUrls
from enums import HTTPProbeCode
from const import verify_url_regex
from db_api import DBAPI


class Scanner:
    def __init__(self, prohibited_urls: Tuple[str],
                  db_adapter: DBAPI, logger: Any):
        self.prohibited_urls = prohibited_urls
        self._db_adapter: DBAPI = db_adapter
        self.logger = logger

    async def _make_probe(self, url: str) -> Union[str, Tuple[str, int, float]]:
        """
        Проверка URL на запрещенные & доступность

        Возвращает один из обьектов HTTPProbeCode при недоступности URL

        Возвращает Tuple[hash str, http code int, latency float] при доступности URL
        """
        if not self.verify_url(url = url):
            return HTTPProbeCode.bad_url
        try:
            start = perf_counter()
            async with ClientSession() as session:
                async with session.get(
                    url = url, 
                    allow_redirects = False,
                    ssl = False
                ) as resp:
                    latency = round(perf_counter() - start, 3)
                    content = await resp.read()
            return (
                sha256(content).hexdigest(), 
                resp.status, 
                latency
            )
        except ConnectionTimeoutError:
            return HTTPProbeCode.no_ok
        except Exception as error:
            self.logger.error(f"error in HTTPClient. {error}")
            return HTTPProbeCode.error

    def verify_url(self, url: str) -> bool:
        """
        Проверка URL на ошибки, protocol scheme & наличие в запрещенных для сканнера URL
        """        
        
        if bool(fullmatch(verify_url_regex, url)):
            url = sub(r'^https?://', '', url)
            url = url.split('/')[0]
            if not url in self.prohibited_urls:
                return True
        if url in self.prohibited_urls:
            self.logger.warning(
                f"{url} requested by tracked. it will be deleted, because its prohibited"
            )
        return False
    
    async def _start_async(self) -> None:
        while True:
            for url in await self._db_adapter.get_urls():
                await self._result_operator(url = url)

    def start(self) -> None:
        run(self._start_async())

    async def _result_operator(self, url: TrackedUrls) -> None:
        """
        Выполняет проверку URL и обрабатывает результат   
        """
        
        history = await self._db_adapter.get_history(limit=1, id=url.id)
        if history and history[0].site:
            if not (datetime.now() - history[0].date) > timedelta(seconds=history[0].site.interval):
                return
            
        probe = await self._make_probe(url = url.url)
        if isinstance(probe, HTTPProbeCode):
            match probe:
                case HTTPProbeCode.no_ok:
                    await self._db_adapter.push_history(is_ok = False, site_id = url.id)
                case HTTPProbeCode.error:
                    await self._db_adapter.push_history(is_ok = False, site_id = url.id)
                case HTTPProbeCode.bad_url:
                    await self._db_adapter.delete_url(username = url.owner, id = url.id)
        else:
            await self._db_adapter.push_history(
                latency = probe[2],
                http_status = probe[1],
                is_ok = True, 
                hash_content = probe[0],
                site_id = url.id
            )