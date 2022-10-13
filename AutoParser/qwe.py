# -*- coding: utf8 -*-
import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}
url = ['http://api.encar.com/search/car/list/premium?count=true&q=(And.Year.range(201800..202299)._.Mileage.range('
       '10000..70000)._.Hidden.N._.CarType.Y._.Trust.Warranty._.Condition.Inspection._.('
       'Or.FuelType.%EB%94%94%EC%A0%A4._.FuelType.%EA%B0%80%EC%86%94%EB%A6%B0.)_.Transmission.%EC%98%A4%ED%86%A0.)&sr'
       '=%7CModifiedDate%7C0%7C50',
       'http://api.encar.com/search/car/list/premium?count=true&q=(And.Year.range('
       '201800..202299)._.Mileage.range('
       '10000..70000)._.Hidden.N._.CarType.N._.Trust.Warranty._.Condition.Inspection._.('
       'Or.FuelType.%EB%94%94%EC%A0%A4._.FuelType.%EA%B0%80%EC%86%94%EB%A6%B0.)_'
       '.Transmission.%EC%98%A4%ED%86%A0.)&sr=%7CModifiedDate%7C0%7C50']
bot = Bot('5644402304:AAHdwG-BJE9ImPiO4RI4nGdxe0jGvU5C7vA')
db = Dispatcher(bot)


@db.message_handler(commands=['start'])
async def new_user(message: types.Message):
    print('Добавил нового пользователя')
    user_id = message.chat.id
    base = sqlite3.connect('user_id.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS user_id(info, zeroinfo)')
    base.commit()
    cur.execute('INSERT INTO user_id VALUES(?, ?)', (user_id, 0))
    base.commit()
    base.close()


@db.message_handler(commands=['stop'])
async def new_user(message: types.Message):
    print('Удалил пользователя')
    user_id = message.chat.id
    base = sqlite3.connect('user_id.db')
    cur = base.cursor()
    cur.execute('DELETE FROM user_id WHERE info = ' + str(user_id))
    base.commit()
    base.close()

executor.start_polling(db, skip_updates=True)
