from asyncio import run

from loader import dp, logger, bot
from const import (
    MIN_INTERVAL, 
    url_up, 
    url_down, 
    hash_change_detected
)

from api import MultiClient
from utils import unformat_username
from datetime import datetime
from asyncio import sleep
from typing import Dict, Any


class Notify:
    def __init__(self, api: MultiClient):
        self.api = api

    async def start(self) -> None:
        while True:
            await self._worker()
            await sleep(MIN_INTERVAL)


    async def _worker(self) -> None:
        for url in await self.api._get_urls_track():
            id = unformat_username(url.username)
            history = await self.api.get_history(id=id, url=url.id)
            if not "2" in history:
                return
            current_time = datetime.now()
            time_difference = current_time - datetime.fromtimestamp(history['1']['date'])
            if time_difference.total_seconds() < history['1']['interval']:
                await self._operator(history=history, user_id=id)

    async def _operator(self, history: Dict[str, Any], user_id: int) -> None:
        if history['1']['is_ok'] and not history['2']['is_ok']:
            await bot.send_message(user_id, url_up(history['1']['url']))
        elif not history['1']['is_ok']:
            await bot.send_message(user_id, url_down(history['1']['url']))
        if history['1']['is_ok']:
            i = next((key for key, entry in history.items() if key != '1' and entry.get('is_ok')), None)           
            if i is not None:
                if history['1']['hash_reqbytes'] != history[i]['hash_reqbytes']:
                    await bot.send_message(
                        user_id,
                        hash_change_detected(
                            (history['1']['hash_reqbytes'], history[i]['hash_reqbytes']),
                            history['1']['url']
                        )
                    )

                                