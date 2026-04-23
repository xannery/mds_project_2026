import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

bot = Bot(token="8664718727:AAHzMm-5mqQu6_VcMATZRbRdF1FaJf02EAY")
dp = Dispatcher()

@dp.message()

async def hello_handler(message = 'Hi'):
    await message.answer('Hello!')

async def echo_handler(message):
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    