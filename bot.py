import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN
from database import MusicDB
from keyboards import play_kb

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = MusicDB()


# START
@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer("🎧 Pepe Music Bot готов!\n\nИспользуй: /search <трек>")


# SEARCH
@dp.message(F.text.startswith("/search"))
async def search(message: Message):
    query = message.text.replace("/search", "").strip()

    if not query:
        await message.answer("Напиши: /search artist or song")
        return

    results = db.search(query)

    if not results:
        await message.answer("Ничего не найдено 😔")
        return

    for r in results:
        music_id, title, artist, _, plays = r

        text = f"🎵 {title} - {artist}\n🔥 plays: {plays}"

        await message.answer(text, reply_markup=play_kb(music_id))


# PLAY
@dp.callback_query(F.data.startswith("play:"))
async def play(callback: CallbackQuery):
    music_id = int(callback.data.split(":")[1])

    track = db.get(music_id)

    if not track:
        await callback.answer("Не найдено")
        return

    _, title, artist, file_id, _ = track

    db.add_play(music_id)

    await callback.message.answer_audio(
        audio=file_id,
        title=title,
        performer=artist or "Unknown"
    )

    await callback.answer()


# MAIN
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())