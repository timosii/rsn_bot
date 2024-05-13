import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, exceptions
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import settings
from controller.general import send_post, send_rsn_post, send_sean_post, when_update
from controller.schedule_tasks import change_ids, check_new_sean_post, control_rus_replies, read_ids
from view.data import HELP_TEXT, REPLY_TEXT

BOT_TOKEN = settings.BOT_TOKEN
MY_ID = settings.MY_ID
RSN_ID = settings.RSN_ID


bot = Bot(BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


def set_scheduler_tasks(bot):
    scheduler.add_job(check_posts, 'interval',
                      next_run_time=datetime.now(),
                      seconds=7200, args=(bot,))
  

async def check_posts(bot: Bot):
    update_sean = check_new_sean_post()
    update_len = control_rus_replies()
    current_sean = read_ids()["Sean"]
    current_len = read_ids()["Len"]
        
    if update_sean and (update_sean > current_sean):
        await bot.send_message(RSN_ID, 'Новый пост от Шона!')
        sean_message = send_sean_post(length_replies=5)
        await bot.send_message(RSN_ID, sean_message, parse_mode="HTML")
        await bot.send_message(MY_ID, 'Новый пост от Шона!')
        try:
            await bot.send_message(MY_ID, sean_message, parse_mode="HTML")
        except exceptions.TelegramBadRequest:
            await bot.send_message(MY_ID, REPLY_TEXT, parse_mode="HTML")
    #else:
    #    await bot.send_message(MY_ID, text="Работаю, нового поста от Шона нет", parse_mode="HTML")
   

    if update_len != current_len and update_len != 0:
        await bot.send_message(RSN_ID, 'Обновление в твоём посте!')
        try:
            rus_message = send_rsn_post(length_replies=5)
            await bot.send_message(RSN_ID, rus_message, parse_mode="HTML")
        except exceptions.TelegramBadRequest:
            await bot.send_message(RSN_ID, REPLY_TEXT, parse_mode="HTML")
            
        await bot.send_message(MY_ID, 'Обновление в твоём посте!')
        try:
            await bot.send_message(MY_ID, rus_message, parse_mode="HTML")
        except exceptions.TelegramBadRequest:
            await bot.send_message(MY_ID, REPLY_TEXT, parse_mode="HTML")
    #else:
    #    await bot.send_message(MY_ID, text="Работаю, обновлений в постах Руса нет", parse_mode="HTML")

    change_ids(update_sean, update_len)
       

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text="Выбери команду:\n/last_post\n/sean\n/ruslan\n/when_update")


@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=HELP_TEXT, parse_mode="HTML")


@dp.message(Command(commands="last_post"))
async def process_last_command(message: Message):
    try:
        reply = send_post(length_replies=5)
        await message.answer(text=reply, parse_mode="HTML")
    except exceptions.TelegramBadRequest:
        reply = REPLY_TEXT
        await message.answer(text=reply, parse_mode="HTML")  


@dp.message(Command(commands="sean"))
async def last_sean_post(message: Message):
    try:
        reply = send_sean_post(length_replies=5)
        await message.answer(text=reply, parse_mode="HTML")
    except exceptions.TelegramBadRequest:
        reply = REPLY_TEXT
        await message.answer(text=reply, parse_mode="HTML")   


@dp.message(Command(commands="ruslan"))
async def last_rsn_post(message: Message):
    try:
        reply = send_rsn_post(length_replies=5)
        await message.answer(text=reply, parse_mode="HTML")
    except exceptions.TelegramBadRequest:
        reply = REPLY_TEXT
        await message.answer(text=reply, parse_mode="HTML")  


@dp.message(Command(commands='when_update'))
async def process_update(message: Message):
    reply = when_update()
    await message.answer(text=reply, parse_mode="HTML")


@dp.message()
async def process_all_answer(message: Message):
    await message.answer(text="Для помощи нажми:\n/help", parse_mode="HTML")
    

async def main():
    set_scheduler_tasks(bot)
    try:
        scheduler.start()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
