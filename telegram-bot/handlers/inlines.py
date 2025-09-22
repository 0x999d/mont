from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile
from asyncio import gather

from fsm import AddURL, ChangeInterval
from const import MIN_INTERVAL, MAX_INTERVAL, \
    no_urls_tracked, choice_url_menu, deleted, \
        url_change_timer, url_info, already_deleted
from const import (
    cancell_text, 
    share_url_text, 
    success_add_url
)
from loader import dp, APIClient
from info import draw_graphic, export_history

from keyboards import (
    cancell,  
    home, 
    get_start,
    my_url_menu, 
    url_menu
)


@dp.callback_query(lambda query: query.data == "cancell")
async def cancell_inl(query: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await query.message.edit_text(cancell_text, reply_markup = home())

@dp.callback_query(lambda query: query.data == "add_url")
async def add_url(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AddURL.url)
    await query.message.edit_text(share_url_text, reply_markup = cancell())
    
@dp.callback_query(
        AddURL.interval,
        lambda query: "interval_set_" in query.data
    )
async def interval_inline_fsm(query: CallbackQuery, state: FSMContext) -> None:
    interval = query.data.split("_")
    if interval[2].isdigit():
        if MIN_INTERVAL <= int(interval[2]) <= MAX_INTERVAL:
            data = await state.get_data()
            try:
                await APIClient.add_url(
                    url = data['url'],
                    id = query.from_user.id,
                    interv = int(interval[2])
                )
            except Exception as error:
                    await query.message.edit_text(
                        str(error), reply_markup=home()
                    )
            else:
                await query.message.edit_text(
                    success_add_url, reply_markup=home()
                )
    await state.clear()

@dp.callback_query(lambda query: "my_url" in query.data)
async def my_url(query: CallbackQuery) -> None:
    urls = await APIClient.get_urls(id = query.from_user.id)
    if urls:
        index = 0
        if not query.data == "my_url":
            index = query.data.split("_")[2]
            if index.isdigit():
                index = int(index)
        await query.message.edit_text(
            choice_url_menu, reply_markup = my_url_menu(
                urls = list(urls.values()), index = index
            )
        )
    else:
        await query.message.edit_text(no_urls_tracked, reply_markup = get_start())

@dp.callback_query(lambda query: "menu_url_" in query.data)
async def menu_url(query: CallbackQuery) -> None:
    id = query.data.split("_")[2]
    if id.isdigit():
        id = int(id) 
        try:
            history, url = await gather(*[
                APIClient.get_history(url = id, id = query.from_user.id),
                APIClient.get_url(url = id, id = query.from_user.id)
            ])
        except:
            await query.message.edit_text(already_deleted, reply_markup=home())
        else:
            graphic = await draw_graphic(list(history.values()))
            if graphic:
                file = BufferedInputFile(
                    file = await draw_graphic(list(history.values())),
                    filename = "result.png"
                )
                await query.message.delete()
                await query.message.answer_photo(
                    photo = file, reply_markup = url_menu(id, True),
                    caption = url_info(url=url, graphic_ready=True)
                )
            else:
                await query.message.edit_text(
                    text = url_info(url=url, graphic_ready=False), 
                    reply_markup=url_menu(id, False)
                )

@dp.callback_query(lambda query: "change_interval_" in query.data)
async def change_interval(query: CallbackQuery, state: FSMContext) -> None:
    id = query.data.split("_")[2]
    if id.isdigit():
        id = int(id)
        await state.set_state(ChangeInterval.interval)
        await state.set_data({"id": id})
        await query.message.delete()
        await query.message.answer(url_change_timer, reply_markup = cancell())

@dp.callback_query(lambda query: "stop_track_" in query.data)
async def stoptrack(query: CallbackQuery) -> None:
    id = query.data.split("_")[2]
    if id.isdigit():
        id = int(id)
        await query.message.delete()
        try:
            await APIClient.delete_url(id = query.from_user.id, url = id) 
        except Exception as error:
            await query.message.answer(str(error), reply_markup = home())
        else:
            await query.message.answer(deleted, reply_markup = home())

@dp.callback_query(lambda query: "export_" in query.data)
async def history_export(query: CallbackQuery) -> None:
    id = query.data.split("_")[1]
    if id.isdigit():
        id = int(id) 
        history = await APIClient.get_history(url = id, id = query.from_user.id)
           
        file = BufferedInputFile(
            file = await export_history(list(history.values())),
            filename = "result.xlsx"
        )
        await query.message.answer_document(document = file)