import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram.filters.command import CommandStart, Command
from db import Database

load_dotenv()

db = Database(os.getenv('DB_URL'))

TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(msg: Message):
    await msg.answer(f"Welcome! {msg.from_user.full_name}")
    if not db.user_exists(msg.from_user.id):
        db.add(msg.from_user.id, msg.from_user.full_name)
    else:
        await msg.answer(f"siz {msg.from_user.full_name} avval ham botga tashrif buyurgansiz ")  # noqa


@dp.message(Command('users'))
async def get_users(msg: Message):
    if msg.from_user.id == int(os.getenv("ADMIN")):
        users = db.get_all_users()
        for x in users:
            await msg.answer(f"UserID: {x[0]} Fullname: {x[1]}")


@dp.message(Command("sendall"))
async def send_msg(msg: Message):
    if msg.chat.type == "private":
        if msg.from_user.id == int(os.getenv("ADMIN")):
            text = msg.text[9:]
            users = db.get_all_users()
            for row in users:
                await bot.send_message(row[0], text)
            await bot.send_message(msg.from_user.id, f"Done message all users")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
