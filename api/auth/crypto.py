from const import generator_wordlist
from random import choice
from passlib.context import CryptContext


class Crypto:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def generate_string(num: int) -> str:
        """
        Генератор случайной строки длиной `num` символов
        """
        return "".join(choice(generator_wordlist) for _ in range(num))

    def create_hash(self, string: str) -> str:
        """
        Хеширует строку с использованием bcrypt
        """
        return self.pwd_context.hash(string)

    def verify_hashes(self, hashed: str, string: str) -> bool:
        """
        Проверяет строку c bcrypt хешем
        """
        return self.pwd_context.verify(string, hashed)