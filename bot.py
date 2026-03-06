import json
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8578660273

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# baza yuklash
try:
    with open("movies.json", "r", encoding="utf-8") as f:
        movies = json.load(f)
except:
    movies = {}

def save_movies():
    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)

# start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎬 <b>Kino botga xush kelibsiz!</b>\n\n"
        "Kino nomi yoki kodini yuboring."
    )

# qidirish
@dp.message()
async def search_movie(message: types.Message):

    if message.text:
        text = message.text.lower()

        # kod orqali
        if text in movies:
            movie = movies[text]

            await message.answer_video(
                video=movie["file_id"],
                caption=f"🎬 <b>{movie['name']}</b>"
            )
            return

        # nom orqali
        results = []

        for code, movie in movies.items():
            if text in movie["name"].lower():
                results.append(f"{code} - {movie['name']}")

        if results:
            await message.answer(
                "🔎 <b>Topilgan kinolar:</b>\n\n" +
                "\n".join(results[:10])
            )
        else:
            await message.answer("❌ Kino topilmadi")

    # admin video yuborsa
    elif message.video and message.from_user.id == ADMIN_ID:

        file_id = message.video.file_id
        new_code = str(len(movies) + 1)

        name = message.caption if message.caption else f"Kino {new_code}"

        movies[new_code] = {
            "name": name,
            "file_id": file_id
        }

        save_movies()

        await message.answer(
            f"✅ Kino qo‘shildi!\n\n"
            f"🎬 Nomi: {name}\n"
            f"🔢 Kod: {new_code}"
        )

async def main():
    print("✅ Bot ishga tushdi")

    while True:
        try:
            await dp.start_polling(bot, skip_updates=True)
        except Exception as e:
            print(f"❌ Xato: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())