from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loader import dp
from const import MAX_INTERVAL, MIN_INTERVAL, url_probe_ok_go_timer, \
      url_added_ok, interval_missed_num_error, interval_change_ok
from keyboards import (
    cancell, 
    home, 
    intervals_beaty
)
from fsm import AddURL, ChangeInterval
from loader import APIClient


@dp.message(AddURL.url)
async def add_url_fsm(message: Message, state: FSMContext) -> None:
    await state.set_state(AddURL.interval)
    await state.set_data({'url': message.text})
    await message.answer(url_probe_ok_go_timer, reply_markup=intervals_beaty(
        min_interval=MIN_INTERVAL,
        max_interval=MAX_INTERVAL
    ))

@dp.message(AddURL.interval)
async def add_url_fsm_intevalstep(message: Message, state: FSMContext) -> None:
    if message.text.isdigit() and MIN_INTERVAL <= int(message.text) <= MAX_INTERVAL:
        data = await state.get_data()
        try:
            await APIClient.add_url(
                                url = data['url'],
                                id = message.from_user.id,
                                interv = int(message.text)
                            )
        except Exception as error:
            await message.answer(str(error), reply_markup=home())
        else:
            await message.answer(url_added_ok, reply_markup = home())
        await state.clear()
    else:
        await message.answer(
            interval_missed_num_error((MIN_INTERVAL, MAX_INTERVAL)), 
            reply_markup = cancell()
        )

@dp.message(ChangeInterval.interval)
async def add_url_fsm_intevalstep(message: Message, state: FSMContext) -> None:
    if message.text.isdigit() and MIN_INTERVAL <= int(message.text) <= MAX_INTERVAL:
        data = await state.get_data()
        await state.clear()
        try:
            await APIClient.update_interval(
                interv = int(message.text), 
                url = data['id'], 
                id = message.from_user.id
            )
        except Exception as error:
            await message.answer(str(error), reply_markup = home())
        else:
            await message.answer(interval_change_ok, reply_markup = home())

    else:
        await message.answer(
            interval_missed_num_error((MIN_INTERVAL, MAX_INTERVAL)), 
            reply_markup = cancell()
        )