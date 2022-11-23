import telebot
import work_with_db

token = '5238517183:AAHkdru03SWwWiPpvzSNFGLXRyXhWKl2wnw'
bot = telebot.TeleBot(token)

def DB_maker(name, link, header, chat_id):
    news = f"❗ {header}\nИсточник: [{str(name)}]({link})"



    bot.send_message(chat_id, news, parse_mode='Markdown', disable_web_page_preview=True)

    print('Новость обновлена - ' + str(name))
    print('__________________________________________________________________')