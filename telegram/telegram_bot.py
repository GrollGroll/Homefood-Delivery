import asyncio
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv
from aiogram.types import Message
import logging

import kafka_consumer

format = '%(asctime)s: %(message)s'
logging.basicConfig(format=format, level=logging.INFO, datefmt='%H:%M:%S')

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

data = kafka_consumer.consume_orders()
user_data = data['user']
order_data = data['order']

massage = f"{user_data.username}, ваш заказ №{order_data.id} поменял статус на {order_data.status}."
chat_id = user_data.telegram_chat_id


async def start_mailing():
    while True:
        try:
            await bot.send_message(chat_id=chat_id, text=massage)
            await asyncio.sleep(1)
        except Exception as e:
            logging.info(f'Не удалось отправить сообщение: {e}')


@dp.message()
async def error_mes(message: Message):
    await message.answer('К сожалению, я вас не понимаю. Я могу только отправлять сообщения.')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_mailing())
    loop.run_until_complete(main())
