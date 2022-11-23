from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#--------------------------------------------------------------------------------------------

meto = [[KeyboardButton(text='Арбатская')],
        [KeyboardButton(text='Театральная')],
        [KeyboardButton(text='Тверская')]]
metro_buttons = ReplyKeyboardMarkup(keyboard = meto, resize_keyboard = True)

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

expansion = [[KeyboardButton(text='👍🏻')],
         [KeyboardButton(text='👎🏻')]]
expansion_buttons = ReplyKeyboardMarkup(keyboard = expansion, resize_keyboard = True)
