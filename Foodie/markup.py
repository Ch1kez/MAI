from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#--------------------------------------------------------------------------------------------

begin = [[KeyboardButton(text='Да')],[KeyboardButton(text='Данила пидор')]]

begin_buttons = ReplyKeyboardMarkup(keyboard = begin, resize_keyboard = True)

#--------------------------------------------------------------------------------------------

metro = [[KeyboardButton(text='Арбатская')],
        [KeyboardButton(text='Театральная')],
        [KeyboardButton(text='Тверская')]]
metro_buttons = ReplyKeyboardMarkup(keyboard = metro, resize_keyboard = True)

#--------------------------------------------------------------------------------------------

kitchen = [[KeyboardButton(text='Европейская')],
           [KeyboardButton(text='Японская')],
           [KeyboardButton(text='Грузинская')]]
kitchen_buttons = ReplyKeyboardMarkup(keyboard = kitchen, resize_keyboard = True)

#--------------------------------------------------------------------------------------------

price = [[KeyboardButton(text='менее 1500')],
         [KeyboardButton(text='1500 - 2000')],
         [KeyboardButton(text='2000 - 3000')]]
price_buttons = ReplyKeyboardMarkup(keyboard = price, resize_keyboard = True)

#--------------------------------------------------------------------------------------------

smile = [[KeyboardButton(text='👍🏻')],
         [KeyboardButton(text='👎🏻')]]
smile_buttons = ReplyKeyboardMarkup(keyboard = smile, resize_keyboard = True)

#--------------------------------------------------------------------------------------------

yes_or_no = [[KeyboardButton(text='Да')],
             [KeyboardButton(text='Нет')]]
yes_or_no_buttons = ReplyKeyboardMarkup(keyboard = yes_or_no, resize_keyboard = True, one_time_keyboard=True)

#--------------------------------------------------------------------------------------------

# skip_buttons = ReplyKeyboardMarkup(one_time_keyboard=False)

#--------------------------------------------------------------------------------------------