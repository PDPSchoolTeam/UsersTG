import os
import json
import asyncio
import logging
from db import Database
from dotenv import load_dotenv
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart, Command
from aiogram.exceptions import TelegramForbiddenError

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


@dp.message(Command('msg', prefix=':'))
async def send_meg(msg: Message):
    await msg.answer("Rasm va rasm sarlavhasini kiriting! ")  # noqa
    if msg.chat.type == "private":
        if msg.from_user.id == int(os.getenv("ADMIN")):
            @dp.message()
            async def upload_img(msg: Message):
                image = msg.json()
                img_link = json.loads(image)
                photo = img_link['photo'][0]['file_id']
                capt = img_link['caption']
                users = db.get_all_users()
                for row in users:
                    user_id = row[0]
                    try:
                        await bot.send_photo(chat_id=user_id, photo=photo, caption=capt)
                    except TelegramForbiddenError:
                        logging.warning(f"User {user_id} blocked the bot. Removing user.")
                        db.remove_users(user_id)
                    except Exception as e:
                        logging.error(f"Failed to send photo to {user_id}: {e}")


# @dp.message()
# async def upload_img(msg: Message):
#     image = msg.json()
#     img_link = json.loads(image)
#     # print(type(img_link))
#     # print(img_link)
#     # print(img_link['photo'][0])
#     photo = img_link['photo'][0]['file_id']
#     capt = img_link['caption']
#     await bot.send_photo(chat_id=msg.chat.id, photo=photo, caption=capt)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
