from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def play_kb(music_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶ Play", callback_data=f"play:{music_id}")]
    ])