from enum import StrEnum

class HTTPProbeCode(StrEnum):
    bad_url = "bad_url" # запрещенная / не прошла проверку regex'ом
    no_ok = "no_ok" # нет ответа // таймаут
    error = "error" # все остальные ошибки http клиента