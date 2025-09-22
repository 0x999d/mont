from fastapi import HTTPException
from fastapi import status

from pydantic import BaseModel, field_validator
from typing import Optional
from re import fullmatch

from const import verify_username_regex, verify_token_regex, verify_password_regex, \
    verify_url_regex, MAX_INTERVAL, MIN_INTERVAL, max_len_url, max_len_password, \
    max_len_username, min_len_password, min_len_username_len


class BaseUsername(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, username: str) -> bool:
        if min_len_username_len <= len(username) <= max_len_username:
            if bool(fullmatch(verify_username_regex, username)):
                return username
            detail = "Bad username"
        else:
            detail = "Your username does not fit the length"
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail)

class ResetPassword(BaseUsername):
    username: str

class BasePassword(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> bool:
        if min_len_password <= len(password) <= max_len_password:
            if bool(fullmatch(verify_password_regex, password)):
                return password
            detail = "Bad password"
        else:
            detail = "Your password does not fit the length"
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail)

class Auth(BaseUsername, BasePassword):
    ...

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    refresh_token: str

    @field_validator("refresh_token")
    @classmethod
    def validate_reftoken(cls, token: str) -> bool:
        if bool(fullmatch(verify_token_regex, token)):
            return token
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Bad token")
    

class ChangeInterval(BaseModel):
    interval: Optional[int] = 5

    def validate_inter(cls, interval: str) -> bool:
        if MIN_INTERVAL <= interval <= MAX_INTERVAL:
            return interval
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 
            f"Only {MIN_INTERVAL} <= x <= {MAX_INTERVAL} allowed"
        )

class BaseURL(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, url: str) -> bool:
        if max_len_url >= len(url):
            if bool(fullmatch(verify_url_regex, url)):
                return url
            detail = "Bad url, please check it"
        else:
            detail = "Very long url"
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail)
    
class DeleteURL(BaseURL):
    ...

class NewURL(BaseURL, ChangeInterval):
    ...

class History(BaseModel):
    id: Optional[int] = None
    limit: Optional[int] = None