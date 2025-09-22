from abc import ABC, abstractmethod

from typing import Any


class HTTPClient(ABC):
    @abstractmethod
    async def _make_request(*args: Any, **kwargs) -> Any:
        ...