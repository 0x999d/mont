from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from loguru import logger

from const import *
from api import MultiClient
from models import Base


load_dotenv()

dp = Dispatcher()

bot = Bot(
        token=getenv("TOKEN_TELEGRAM_BOT"), 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

logger.add(
    sink = logs_path,
    level = logs_level,
    rotation = max_logs_size
)

APIClient = MultiClient(
    api_url=API_URL,
    db_url=getenv("DB_CONNECT_URL"),
    chiper_key=getenv("CIPHER_KEY"),
    logger=logger,
    tables=Base
    )