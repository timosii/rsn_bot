from aiogram import Bot, Dispatcher, exceptions
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import settings
from formatter import HELP_TEXT
from general import send_post, send_rsn_post, send_sean_post, when_update

BOT_TOKEN = settings.BOT_TOKEN
MY_ID = settings.MY_ID
RSN_ID = settings.RSN_ID

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=
        "Выбери команду:\n/last_post\n/sean\n/ruslan\n/when_update"
    )


@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(
        text=HELP_TEXT
    )


@dp.message(Command(commands="last_post"))
async def process_last_command(message: Message):
    reply = send_post()
    await message.answer(text=reply, parse_mode="HTML")


@dp.message(Command(commands="sean"))
async def process_three_command(message: Message):
    try:
        reply = send_sean_post()
        await message.answer(text=reply, parse_mode="HTML")
    except exceptions.TelegramBadRequest:
        try:
            reply = send_sean_post(length_replies=4)
            await message.answer(text=reply, parse_mode="HTML")
        except exceptions.TelegramBadRequest:
            try:
                reply = send_sean_post(length_replies=3)
                await message.answer(text=reply, parse_mode="HTML")
            except exceptions.TelegramBadRequest:
                raise


@dp.message(Command(commands="ruslan"))
async def process_three_RSN_command(message: Message):
    try:
        reply = send_rsn_post()
        await message.answer(text=reply, parse_mode="HTML")
    except exceptions.TelegramBadRequest:
        try:
            reply = send_rsn_post(length_replies=4)
            await message.answer(text=reply, parse_mode="HTML")
        except exceptions.TelegramBadRequest:
            try:
                reply = send_rsn_post(length_replies=3)
                await message.answer(text=reply, parse_mode="HTML")
            except exceptions.TelegramBadRequest:
                raise
            

@dp.message(Command(commands='when_update'))
async def process_update(message: Message):
    reply = when_update()
    await message.answer(text=reply, parse_mode="HTML")


@dp.message()
async def process__all_answer(message: Message):
    await message.answer(text="Для помощи нажми:\n/help", parse_mode="HTML")
    

if __name__ == '__main__':
    dp.run_polling(bot)
