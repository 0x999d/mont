from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from typing import Union

from loader import dp, APIClient
from keyboards import get_start
from const import hello_text


@dp.message(CommandStart())
@dp.callback_query(lambda query: query.data == "home")
async def start(message: Union[Message, CallbackQuery]) -> None:
    user = await APIClient.get_urls(id=message.from_user.id)
    if isinstance(message, CallbackQuery):
        send = message.message.edit_text
        if message.message.photo:
            await message.message.delete()
            send = message.message.answer
    else:
        send = message.answer
    await send(
        text = hello_text(message.from_user.first_name), 
        reply_markup = get_start(bool(user))
        )