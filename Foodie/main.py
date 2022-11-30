from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from Parse_Rests import get_rests_info
import markup

bot = Bot('5886258157:AAHp1JqgOLM2Opam5vJHztVHd1GrlgDgGFE')
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    void = State()
    begin = State()
    metro = State()
    kitchen = State()
    price = State()
    smile = State()
    end = State()


# -----------------------------------------------------------------------------------------------------------------------
@dp.message_handler(lambda message: message, state=UserState.begin)
async def start_invalid(message: types.Message):
    if await menu(message.text):
        return await metro(message)
    else:
        return await start(message)


@dp.message_handler(lambda message: message, state=UserState.metro)
async def metro_invalid(message: types.Message, state: FSMContext):
    if message.text not in ["Арбатская", "Театральная", "Тверская"]:
        if await menu(message.text):
            await UserState.begin.set()
            return await metro(message)
        else:
            await UserState.begin.set()
            return await metro(message)
    else:
        if message.text == "Арбатская":
            await state.update_data(chosen_metro=1)
        elif message.text == "Театральная":
            await state.update_data(chosen_metro=2)
        elif message.text == "Тверская":
            await state.update_data(chosen_metro=3)
        user_sub = await state.get_data()
        print(user_sub)
        await UserState.metro.set()
        return await kitchen(message)


@dp.message_handler(lambda message: message, state=UserState.kitchen)
async def kitchen_invalid(message: types.Message, state: FSMContext):
    if message.text not in ["Европейская", "Японская", "Грузинская"]:
        if await menu(message.text):
            await UserState.begin.set()
            return await metro(message)
        else:
            return await kitchen(message)
    else:
        if message.text == "Европейская":
            await state.update_data(chosen_kitchen=1)
        elif message.text == "Японская":
            await state.update_data(chosen_kitchen=2)
        elif message.text == "Грузинская":
            await state.update_data(chosen_kitchen=3)
        await UserState.metro.set()
        user_kit = await state.get_data()
        print(user_kit)
        await UserState.kitchen.set()
        return await price(message)


@dp.message_handler(lambda message: message, state=UserState.price)
async def price_invalid(message: types.Message, state: FSMContext):
    if message.text not in ["менее 1500", "1500 - 2000", "2000 - 3000"]:
        if await menu(message.text):
            await UserState.begin.set()
            return await metro(message)
        else:
            await UserState.kitchen.set()
            return await price(message)
    else:
        if message.text == "менее 1500":
            await state.update_data(chosen_price=1)
        elif message.text == "1500 - 2000":
            await state.update_data(chosen_price=2)
        elif message.text == "2000 - 3000":
            await state.update_data(chosen_price=3)
        await UserState.price.set()

        user_kit = await state.get_data()
        arr = get_rests_info(user_kit["chosen_metro"], user_kit["chosen_kitchen"], user_kit["chosen_price"])
        print(arr)
        for el in arr:
            await message.answer(el, parse_mode=types.ParseMode.MARKDOWN_V2, disable_web_page_preview=False)

        return await smile(message)


@dp.message_handler(lambda message: message, state=UserState.smile)
async def smile_invalid(message: types.Message):
    if message.text not in ["👍🏻", "👎🏻"]:
        if await menu(message.text):
            await UserState.begin.set()
            return await metro(message)
        else:
            await UserState.price.set()
            return await smile(message)
    else:
        if message.text == "👍🏻":
            await message.answer('Спасибо за Ваш ответ! Не останавливайте бота и мы '
                                 'свяжемся с вами, как только он станет еще хоть чуточку умнее!')
        else:
            await message.answer('Спасибо за Ваш ответ! Мы сделаем все, чтобы в будущем '
                                 'наш продукт покорил и ваше сердце.')

        await UserState.price.set()
        return await yes_or_no(message)


@dp.message_handler(lambda message: message, state=UserState.end)
async def yes_or_no_invalid(message: types.Message):
    if message.text not in ["Да", "Нет"]:
        if await menu(message.text):
            await UserState.begin.set()
            return await metro(message)
        else:
            await UserState.price.set()
            return await yes_or_no(message)
    else:
        if message.text == 'Да':
            await UserState.begin.set()
            return await metro(message)
        else:
            await UserState.void.set()
            return await message.answer('Если вновь захотите воспользоваться услугами бота, '
                                        'нажмите /change_filter.\nДо скорых встреч!')


@dp.message_handler(lambda message: message, state=UserState.void)
async def void_invalid(message: types.Message):
    if await menu(message.text):
        await UserState.begin.set()
        return await metro(message)


# Проверка кнопки '/change_filter'
async def menu(msg_txt):
    if msg_txt == '/change_filter':
        return True
    else:
        return False


###################################      СТАРТ
async def start(msg):
    await UserState.begin.set()
    await msg.answer('Нажмите /change_filter для начала поиска заведения!')


# Обработчик кнопки start
@dp.message_handler(commands='start')
async def start_handler(message: types.Message):
    await start(message)


###################################

###################################      МЕТРО
async def metro(msg):
    await UserState.metro.set()
    await msg.answer('Рядом с какой станцией '
                     'метро Вы бы хотели покушать?',
                     reply_markup=markup.metro_buttons)


# Обработчик состояния 'метро'
@dp.message_handler(state=UserState.begin)
async def metro_handler(message: types.Message):
    await metro(message)


###################################

###################################      КУХНЯ
async def kitchen(msg):
    await UserState.kitchen.set()
    await msg.answer('Какая кухня Вам сегодня по душе?',
                     reply_markup=markup.kitchen_buttons)


###################################      СРЕДНИЙ ЧЕК
async def price(msg):
    await UserState.price.set()
    await msg.answer('Заведения с каким средним чеком Вас интересуют?',
                     reply_markup=markup.price_buttons)


###################################      СМАЙЛ
async def smile(msg):
    await UserState.smile.set()
    await msg.answer('Хотели бы Вы, чтобы наш робот расширил географию своей '
                     'работы и увеличил критерии подбора?',
                     reply_markup=markup.smile_buttons)


###################################      КОНЕЦ
async def yes_or_no(msg):
    await UserState.end.set()
    await msg.answer('Хотите повторно выбрать заведение?',
                     reply_markup=markup.yes_or_no_buttons)


if __name__ == '__main__':
    executor.start_polling(dp)
