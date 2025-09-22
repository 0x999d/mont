from dotenv import load_dotenv
from os import getenv

from fastapi import FastAPI
from loguru import logger

from models import DB
from db_api import DBAPI
from auth import JWT
from const import *
from scanner import Scanner


load_dotenv()

DBAdapter = DBAPI(
        tables=DB, 
        db_url=getenv("DB_CONNECT_URL"),
        logger=logger
    )

app = FastAPI()

JWTManager = JWT(
    private_key_path=private_key,
    public_key_path=public_key,
    access_token_exp_minutes=access_token_exp_minutes,
    refresh_token_exp_days=refresh_token_exp_days
)

logger.add(
    sink = logs_path,
    level = logs_level,
    rotation = max_logs_size
)

HTTPScanner = Scanner(
    prohibited_urls=prohibited_urls, 
    db_adapter=DBAdapter,
    logger=logger
)