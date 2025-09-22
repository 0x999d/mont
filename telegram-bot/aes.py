from base64 import b64encode, b64decode
from hashlib import sha256
from Crypto import Random
from Crypto.Cipher import AES

from models.crypto import Cipher


class CipherAES(Cipher):
    def __init__(self, key: str):
        self.bs = AES.block_size  
        self.key = sha256(key.encode()).digest() 

    def encrypt(self, raw: str) -> str:
        raw_padded = self._pad(raw)
        iv = Random.new().read(self.bs)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(raw_padded.encode('utf-8'))
        return b64encode(iv + encrypted).decode('utf-8')

    def decrypt(self, enc: str) -> str:
        enc = b64decode(enc)
        iv = enc[:self.bs]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(enc[self.bs:])
        return self._unpad(decrypted).decode('utf-8')

    def _pad(self, s: str) -> str:
        pad_len = self.bs - len(s.encode('utf-8')) % self.bs
        return s + chr(pad_len) * pad_len

    def _unpad(self, s: bytes) -> bytes:
        return s[:-s[-1]]