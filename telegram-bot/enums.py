from enum import StrEnum


class HTTPMethod(StrEnum):
    post = "POST"
    get = "GET"
    delete = "DELETE"
    patch = "PATCH"

class GetToken(StrEnum):
    ok = "ok"
    need_refresh = "need_refresh"
    need_new = "need_new"