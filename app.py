import logging
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from selenium import webdriver
import schedule
import time
import ast
import asyncio


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-sh-usage')

driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)
driver.implicitly_wait(4)

URL = 'https://hh.ru/'

launch = True




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
    await message.answer("Bot AIO_hh_wakeUp works")


@dp.message_handler(commands=['res'])
async def res(message: types.Message):
    await message.answer("RES AIO_Bot starts to work")

    # start_res()
    # wake_up()
    #
    # bot_schedule()

    await start_res()
    await wake_up()
    await bot_schedule()



@dp.message_handler(commands=['stop'])
async def stop_res(message: types.Message):
    global launch
    launch = False
    await message.answer("STOP is activated")


async def start_res():

    global launch
    launch = True



async def wake_up():

    await bot.send_message(227722043, "Function Wake_up starts")
    driver.get(URL)

    hh_add = os.environ.get('hh')

    testarray = ast.literal_eval(hh_add)


    for cook in testarray:
        driver.add_cookie(cook)

    await asyncio.sleep(2)
    driver.refresh()
    await asyncio.sleep(1)


    # cookies = pickle.load(open("session", "rb"))
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    # driver.refresh()

    ob = driver.find_elements_by_class_name("HH-Supernova-NaviLevel2-Link")
    ob[0].click()

    ob1 = driver.find_elements_by_class_name('bloko-link_dimmed')

    await bot.send_message(227722043, "here 2222222")


    for i in ob1:
        if i.text == 'Поднять в поиске':
            try:
                i.click()
                await bot.send_message(-1001364950026, 'Подняли! :)')
            except:
                await bot.send_message(-1001364950026, 'Что то не подняли :(')

    await bot.send_message(227722043, "Function Wake_up finished")



async def bot_schedule():
    schedule.every(250).minutes.do(wake_up)

    while launch:
        schedule.run_pending()
        await asyncio.sleep(1)




async def on_startup(dp):
    logging.warning('Starting connection')
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)

