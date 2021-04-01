import logging
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

TOKEN = os.getenv('TOKEN')
PROJECT_NAME = os.getenv('PROJECT_NAME')

WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com'
WEBHOOK_PATH = '/' + TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')



logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def main_start(message: types.Message):
    await message.reply(text='бла бла бла', reply=True)


@dp.message_handler(commands=['help'])
async def send_message(message: types.Message):
    await message.reply('Привет!\nЯ - эхобот')
    await main_start(message=message)



#
# @dp.message_handler(content_types=['text'])
# async def main_2(message : types.Message):
#     await bot.send_message(message.from_user.id, 'Приветики ))')


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def main_text(message: types.Message):
    text = message.text
    if text and not text.startswith('/'):
        await message.reply(text=text)



@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


async def on_startup(dp):
    logging.warning('Starting connection')
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)

