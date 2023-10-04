import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from bs4 import BeautifulSoup as BS

from config import settings

BOT_TOKEN = settings.BOT_TOKEN
MY_ID = settings.MY_ID
RSN_ID = settings.RSN_ID

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


def form_response():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
    } 
    url = "https://www.infinitestudio.art/posts.php?discussion=2"
    response = requests.get(url, headers=headers) 
    soup = BS(response.text, "lxml")
    result = soup.find_all("div", 'posts')
    return result




@dp.message(CommandStart())
async def process_start_command(message: Message):
    print(form_response())
    # await bot.send_message(MY_ID, form_response())
    # await message.answer(text="Привет, брат! Брат моего брата - мой брат")


@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    form_message = f"Username: {message.from_user.username}\nid: {message.from_user.id}\nБот: {'Да' if message.from_user.is_bot else 'Нет'}\nИмя: {message.from_user.first_name}\nФамилия: {message.from_user.last_name}"
    await bot.send_message(MY_ID, form_message)
    await message.answer(text="Отправляю сообщения пользователя Sean Brakefield c форума infinite_studio.art. Нахожусь в разработке")


@dp.message()
async def process_day_command(message: Message):
    form_message = f"Username: {message.from_user.username}\nid: {message.from_user.id}\nБот: {'Да' if message.from_user.is_bot else 'Нет'}\nИмя: {message.from_user.first_name}\nФамилия: {message.from_user.last_name}"
    await bot.send_message(MY_ID, form_message)
    await message.answer(text="Пока не умею ничего. Разрабатываюсь")


if __name__ == '__main__':
    dp.run_polling(bot)