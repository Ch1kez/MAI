import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from RgRu import main_RgRu
from PrimeRu import main_PrimeRu
from LentaRu import main_LentaRu
import config
import work_with_db

bot = Bot(config.token)
dp = Dispatcher(bot)
db = work_with_db.DataBaseWork()

async def mess():
    while True:
        await asyncio.sleep(60)
        print('Время пришло!')
        checking_for_new_news()

@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    kbd_btn = [[types.KeyboardButton(text='Rg.ru')],
               [types.KeyboardButton(text='Prime.ru')],
               [types.KeyboardButton(text='Lenta.ru')]]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kbd_btn,
        resize_keyboard=True)

    if db.is_exist_user_in_db(message.from_user.id) == False:
        db.add_user_in_users_table(message.from_user.id, message.from_user.first_name)
        await message.answer('Бот запущен!')

    await message.answer("Выберите источник, с которого вы хотите получить новость!",
                         reply_markup=keyboard)

@dp.message_handler()
async def buttons_is_pressed(message: types.Message):
    sourse_name = ''

    if message.text == 'Rg.ru':
        sourse_name = ['RgRu', 'rgru_received']

    elif message.text == 'Prime.ru':
        sourse_name = ['PrimeRu', 'primeru_received']

    elif message.text == 'Lenta.ru':
        sourse_name = ['LentaRu', 'lenta_received']

    else:
        await message.answer('Я не понимаю Вас!')
        return

    if db.is_user_received_current_news(message.from_user.id, sourse_name[1]) == False:
        data = db.getting_news_from_db(sourse_name[0])
        db.update_received_news_for_current_user(message.from_user.id, sourse_name[1], True)
        news = f"❗ {data[2]}\n{data[1]}\nИсточник: [{data[0]}]({data[3]})"
        await bot.send_message(message.chat.id, news, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await message.answer('Новых новостей с этого источника пока нет!')

def check_for_exists_news_in_db(name, header, date, link):
    buff = db.is_exist_news_in_db(name, header)

    if buff == 0: # Такая новость есть в бд
        return False

    elif buff == 1: # В бд есть старая новость от этого источника
        db.delete_news_from_news_table(name)
        db.add_news_in_news_table(name, header, date, link)
        print(f'Появилась новая запись из {name}!')
        return True

    elif buff == 2: # В бд нет новостей от этого источника
        db.add_news_in_news_table(name, header, date, link)
        return True

def checking_for_new_news():
    [name, header, date, link] = main_RgRu()
    check = check_for_exists_news_in_db(name, header, date, link)
    if check == True:
        db.update_received_news_for_all_users('rgru_received', False)

    [name, header, date, link] = main_PrimeRu()
    check = check_for_exists_news_in_db(name, header, date, link)
    if check == True:
        db.update_received_news_for_all_users('primeru_received', False)

    [name, header, date, link] = main_LentaRu()
    check = check_for_exists_news_in_db(name, header, date, link)
    if check == True:
        db.update_received_news_for_all_users('lenta_received', False)

def launching_db():
    db.create_db()
    db.create_table_users()
    db.create_table_news()

    checking_for_new_news()

if __name__ == '__main__':
    launching_db()
    loop = asyncio.get_event_loop()
    loop.create_task(mess())
    executor.start_polling(dp)