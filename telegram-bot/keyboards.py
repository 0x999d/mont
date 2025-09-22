from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from typing import Optional


def get_start(sites_exists: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if sites_exists:
        builder.button(text = "🗂️ Мои URL", callback_data = "my_url")
    builder.button(text = "➕ Добавить URL", callback_data = "add_url")
    
    builder.adjust(1)
    return builder.as_markup()

def cancell(data: Optional[str] = "cancell") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = "❌ Отменить", callback_data = data)
    return builder.as_markup()

def home() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = "🏠 Меню", callback_data = "home")
    return builder.as_markup()

def intervals_beaty(min_interval: int, max_interval: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = f"{min_interval} sec", callback_data = f"interval_set_{min_interval}")
    builder.button(text = f"{max_interval // 2} sec", callback_data = f"interval_set_{int(max_interval / 2)}")
    builder.button(text = f"{max_interval} sec", callback_data = f"interval_set_{max_interval}")
    builder.adjust(2, 1)
    return builder.as_markup()

def my_url_menu(urls: list, index: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    start = index * 5
    end = start + 5
    slice = urls[start:end]

    for url in slice:
        builder.button(text = url['url'], callback_data = f"menu_url_{url['id']}")
    if end < len(urls):
        builder.button(text="➡️ Дальше", callback_data=f"my_url_{index + 1}")
    if start > 0:
        builder.button(text="⬅️ Назад", callback_data=f"my_url_{index - 1}")
    builder.button(text = "🏠 Меню", callback_data = "home") 
    
    shift = [1 for _ in range(len(slice))]
    builder.adjust(*shift, 2)
    return builder.as_markup()

def url_menu(id: int, export_allow: Optional[bool] = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = "⏱️ Изменить интервал", callback_data = f"change_interval_{id}") 
    builder.button(text = "❌ Перестать отслеживать", callback_data = f"stop_track_{id}") 
    if export_allow:
        builder.button(text = "📤 Экспортировать в XLSX", callback_data = f"export_{id}")
    builder.button(text = "🏠 Меню", callback_data = "home") 
    builder.adjust(1)
    return builder.as_markup()