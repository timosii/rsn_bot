import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, exceptions
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from background import keep_alive
from config import settings
from general import send_post, send_rsn_post, send_sean_post, when_update
from logic.base_logic import post_and_replies
from schedule_tasks import check_last_sean_post
from view import HELP_TEXT

BOT_TOKEN = settings.BOT_TOKEN
MY_ID = settings.MY_ID
RSN_ID = settings.RSN_ID


bot = Bot(BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

last_post_id = "11549"


def set_scheduler_tasks(bot):
    scheduler.add_job(check_updates_interval, 'interval', next_run_time=datetime.now(), seconds=7200, args=(bot,))


def change_last_id(id):
    global last_post_id
    last_post_id = id
    

async def check_updates_interval(bot: Bot):
    update_post_id = check_last_sean_post()    
    if update_post_id and (last_post_id != update_post_id):
        await bot.send_message(RSN_ID, 'Новый пост от Шона!')
        sean_message = post_and_replies(update_post_id)
        await bot.send_message(MY_ID, sean_message, parse_mode="HTML")
        await bot.send_message(RSN_ID, sean_message, parse_mode="HTML")
        change_last_id(update_post_id)
        

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text="Выбери команду:\n/last_post\n/sean\n/ruslan\n/when_update")


@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=HELP_TEXT, parse_mode="HTML")


@dp.message(Command(commands="last_post"))
async def process_last_command(message: Message):
    length_replies = 5
    while True:
        try:
            reply = send_post(length_replies=length_replies)
            await message.answer(text=reply, parse_mode="HTML")
            break
        except exceptions.TelegramBadRequest:
            length_replies -= 1
            if length_replies == 0:
                reply = "К сожалению, текст постов слишком большой, придётся  сходить на форум ☹️ <a href='https://www.infinitestudio.art/posts.php?discussion=-1'>Вот ссылка</a>"
                await message.answer(text=reply, parse_mode="HTML")
                break


@dp.message(Command(commands="sean"))
async def process_three_command(message: Message):
    length_replies = 5
    while True:
        try:
            reply = send_sean_post(length_replies=length_replies)
            await message.answer(text=reply, parse_mode="HTML")
            break
        except exceptions.TelegramBadRequest:
            length_replies -= 1
            if length_replies == 0:
                reply = "К сожалению, текст постов слишком большой, придётся  сходить на форум ☹️ <a href='https://www.infinitestudio.art/posts.php?discussion=-1'>Вот ссылка</a>"
                await message.answer(text=reply, parse_mode="HTML")
                break


@dp.message(Command(commands="ruslan"))
async def process_three_RSN_command(message: Message):
    length_replies = 5
    while True:
        try:
            reply = send_rsn_post(length_replies=length_replies)
            await message.answer(text=reply, parse_mode="HTML")
            break
        except exceptions.TelegramBadRequest:
            length_replies -= 1
            if length_replies == 0:
                reply = "К сожалению, текст постов слишком большой, придётся  сходить на форум ☹️ <a href='https://www.infinitestudio.art/posts.php?discussion=-1'>Вот ссылка</a>"
                await message.answer(text=reply, parse_mode="HTML")
                break


@dp.message(Command(commands='when_update'))
async def process_update(message: Message):
    reply = when_update()
    await message.answer(text=reply, parse_mode="HTML")


@dp.message()
async def process__all_answer(message: Message):
    await message.answer(text="Для помощи нажми:\n/help", parse_mode="HTML")


async def main():
    set_scheduler_tasks(bot)
    try:
        scheduler.start()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


keep_alive()
if __name__ == '__main__':
    asyncio.run(main())
