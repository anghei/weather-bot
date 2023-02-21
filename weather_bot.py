from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import os
from dotenv import load_dotenv
from main import get_mkp, get_krd
from time import sleep

load_dotenv()


bot = Bot(token=os.getenv("TELEGRAM_TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['Краснодар', 'Майкоп']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)

    await message.answer('Выберите город для получения прогноза погоды', reply_markup=keyboard)


@dp.message_handler(Text(equals='Майкоп'))
async def mkp(message: types.Message):
    await message.answer(text=get_mkp())


@dp.message_handler(Text(equals='Краснодар'))
async def krd(message: types.Message):
    await message.answer(text=get_krd())

def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()