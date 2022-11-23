import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import markup

bot = Bot('5886258157:AAHp1JqgOLM2Opam5vJHztVHd1GrlgDgGFE')
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def from_start_to_menu(message: types.Message):
    await message.answer('Добрый день! Рядом с какой станцией'
                         ' метро Вы бы хотели покушать?',
                         reply_markup = markup.metro_buttons)

@dp.message_handler()
async def menu_handler(message: types.Message):
    metro_is_pressed = False
    kitchen_is_pressed = False
    expansion_is_pressed = False
    up_down = False

    if message.text == 'Арбатская':
        metro_is_pressed = True
    elif message.text == 'Театральная':
        metro_is_pressed = True
    elif message.text == 'Тверская':
        metro_is_pressed = True

    if message.text == 'Европейская':
        kitchen_is_pressed = True
    elif message.text == 'Японская':
        kitchen_is_pressed = True
    elif message.text == 'Грузинская':
        kitchen_is_pressed = True

    if message.text == 'менее 1500':
        expansion_is_pressed = True
    elif message.text == '1500 - 2000':
        expansion_is_pressed = True
    elif message.text == '2000 - 3000':
        expansion_is_pressed = True

    if message.text == '👍🏻':
        await message.answer('Спасибо за Ваш ответ! Не останавливайте'
                             ' бота и мы свяжемся с вами, как только'
                             ' он станет еще хоть чуточку умнее!')
        up_down = True

    elif message.text == '👎🏻':
        await message.answer('Спасибо за Ваш ответ! Мы сделаем все,'
                             ' чтобы в будущем наш продукт покорил и'
                             ' ваше сердце.')
        up_down = True


    if metro_is_pressed == True:
        await message.answer('Отлично! Какая кухня Вам сегодня по душе?',
                             reply_markup = markup.kitchen_buttons)

    if kitchen_is_pressed == True:
        await message.answer('Заведения с каким средним чеком Вас интересуют?',
                             reply_markup = markup.price_buttons)

    if expansion_is_pressed == True:
        await message.answer('***выдаем ссылки на заведения по выбранным критериям***')
        await message.answer('Хотели бы Вы, чтобы наш робот расширил географию своей'
                             ' работы и увеличил критерии подбора?',
                             reply_markup = markup.expansion_buttons)

    if up_down == True:
        await message.answer('Хотите продолжить? Если да, то на какой станцией'
                             ' метро Вы бы хотели покушать?',
                             reply_markup=markup.metro_buttons)

if __name__ == '__main__':
    executor.start_polling(dp)