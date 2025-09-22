from abc import ABC, abstractmethod
from typing import Any


class Cipher(ABC):
    @abstractmethod
    def encrypt(*args: Any, **kwargs: Any) -> Any:
        ...

    @abstractmethod
    def decrypt(*args: Any, **kwargs: Any) -> Any:
        ...
    