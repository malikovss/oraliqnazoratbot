from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def change_answer(id: int):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Yangilash🔄", callback_data=f"cans_u_{id}"),
        InlineKeyboardButton("Bekor qilish❌", callback_data=f"cans_d"),
    )
    return markup