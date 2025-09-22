from jose import jwt 

from typing import Union, Callable, Any
from datetime import datetime, timezone
from random import choice

from asyncio import get_event_loop
from concurrent.futures import ThreadPoolExecutor

from const import password_wordlist


def get_exp_datetime(token: str) -> Union[datetime, None]:
    decoded = jwt.get_unverified_claims(token)

    exp = decoded.get("exp")
    if exp:
        dt = datetime.fromtimestamp(exp, timezone.utc)
        return dt
    return

def format_username(id: int) -> str:
    return f"user{id}"

def unformat_username(id: str) -> int:
    return int(id[4:])

def generate_password(len: int) -> str:
    return "".join([choice(password_wordlist) for _ in range(len)])

def sync_to_async(func: Callable[[Any, Any], Any]):
    async def wrapper(*args, **kwargs):
        loop = get_event_loop()
        with ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(executor, func, *args, **kwargs)
    return wrapper