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
import aioschedule
from aiogram.utils.exceptions import BotBlocked


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-sh-usage')

driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)
driver.implicitly_wait(4)

URL = os.getenv('URL')
URL2 = os.getenv('URL2')


launch = True

test_group = -1001153348142
test = -1001364950026
me = os.getenv('me')


TOKEN = os.getenv('TOKEN')
PROJECT_NAME = os.getenv('PROJECT_NAME')

WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com'
WEBHOOK_PATH = '/' + TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')


logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def main_start(message: types.Message):
    await message.answer("Bot AIO_hh_wakeUp works")


@dp.message_handler(commands=['res'])
async def res(message: types.Message):
    await message.answer("RES AIO_Bot starts to work")
    await wake_up()


@dp.message_handler(commands=['res2'])
async def res2(message: types.Message):
    await message.answer("RES2 AIO_Bot starts to work")
    await start_res()
    asyncio.create_task(bot_schedule())



@dp.message_handler(commands=['stop'])
async def stop_res(message: types.Message):

    global launch
    launch = False
    await bot.send_message(me, "STOP is activated")



async def start_res():

    global launch
    launch = True
    await bot.send_message(me, "launch is True")



async def wake_up():

    try:

        await bot.send_message(test_group, "Function Wake_up starts")


        driver.get(URL)

        hh_cookies = os.environ.get('hh')

        testarray = ast.literal_eval(hh_cookies)

        for cook in testarray:
            driver.add_cookie(cook)

        await asyncio.sleep(1)
        driver.refresh()
        await asyncio.sleep(1)

        # cookies = pickle.load(open("session", "rb"))
        # for cookie in cookies:
        #     driver.add_cookie(cookie)
        # driver.refresh()

        await bot.send_message(test_group, 'before search')

        ob = driver.find_elements_by_class_name("HH-Supernova-NaviLevel2-Link")

        await bot.send_message(test_group, f'length of ob = {len(ob)}')
        
        try:
            ob[0].click()
        except:
            driver.get(URL2)

        ob1 = driver.find_elements_by_class_name('bloko-link_dimmed')

        await bot.send_message(test_group, f'length of ob1 = {len(ob1)}')


        # if len(ob1) > 0:
        for i in ob1:
            if i.text == 'Поднять в поиске':
                try:
                    i.click()
                    await bot.send_message(test_group, 'Cool! Raised successfully')
                except:
                    await bot.send_message(test_group, "Ups, couldn't raise :(")
                # else:
                #     pass

        await bot.send_message(test_group, 'after search')

    except Exception as e:

        await bot.send_message(test_group, e)

        

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)


async def bot_schedule():
    try:
        aioschedule.every(60).minutes.do(wake_up)
        # aioschedule.every(80).seconds.do(wake_up)
        while launch:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
    except Exception as e:
        await bot.send_message(me, e)



async def on_startup(dp):
    logging.warning('Starting connection')
    await bot.set_webhook(WEBHOOK_URL)
    # asyncio.create_task(bot_schedule())


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT, skip_updates=True)

